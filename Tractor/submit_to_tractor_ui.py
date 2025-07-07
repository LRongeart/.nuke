import nuke
import getpass
import os
import tractor
import tractor.api.query as tq
#from tractor.base.api.query import jobs
from tractor.base.api.author import Job, Task
import subprocess
import sys
import json

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import isValid

# Global reference to prevent garbage collection
submit_ui_instance = None
username = getpass.getuser()
tractorSpoolVersion = "v1.0"
tractorSpoolWindowTitle = 'TractorSpool {}'.format(tractorSpoolVersion)
tractorSpoolHelpWindowTitle = 'TractorSpool Help {}'.format(tractorSpoolVersion)
contactLR = "loucas.rongeart@gmail.com"

SIMTRACKER = {"user": "root", #  !!!! TO ENABLE ONCE READY !!!!
                  "password": ""}

def spool_job_via_bridge(job_data, owner="3d4", filename=None):
    # Path to your portable Python 2.7 executable and bridge script
    python2_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\python2.7_portable\App\Python\python.exe"
    bridge_script = r"//tls-storage02/Install/NUKE/Nuke_PLUG/.nuke_DEV/tractor/tractor_spool_bridge.py"

    # Build command arguments
    cmd_args = [python2_path, bridge_script, owner]
    if filename:
        cmd_args.append(filename)

    print(f"[DEBUG] Bridge command: {' '.join(cmd_args)}")
    print(f"[DEBUG] Job data length: {len(job_data)} bytes")

    # Launch the bridge as a subprocess
    proc = subprocess.Popen(
        cmd_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = proc.communicate(input=job_data.encode('utf-8'))
    
    print(f"[DEBUG] Bridge return code: {proc.returncode}")
    print(f"[DEBUG] Bridge stdout: {out.decode('utf-8')}")
    print(f"[DEBUG] Bridge stderr: {err.decode('utf-8')}")
    
    if proc.returncode != 0:
        raise RuntimeError(f"Bridge error (code {proc.returncode}): {err.decode('utf-8')}")
    
    try:
        result_data = json.loads(out.decode('utf-8'))
        if "error" in result_data:
            raise RuntimeError(f"Bridge reported error: {result_data['error']}")
        return result_data["result"]
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse bridge output as JSON: {e}")
        print(f"[ERROR] Raw output: {out.decode('utf-8')}")
        raise RuntimeError(f"Invalid JSON response from bridge: {e}")

def get_blade_info():
    """Query available blades and their services/envkeys for debugging"""
    try:
        tq.setEngineClientParam(user=SIMTRACKER["user"], password=SIMTRACKER["password"])
        
        # Try the simplest blade query first
        try:
            blades = tq.blades()
            print(f"[DEBUG] Successfully queried {len(blades) if blades else 0} blades")
        except Exception as e:
            print(f"[ERROR] tq.blades() failed: {e}")
            # Try to get blade info from job/engine queries instead
            try:
                print("[DEBUG] Attempting alternative blade discovery...")
                # This might not work but worth trying
                from tractor.api.query import EngineClient
                ec = EngineClient()
                # Try to get engine status which might include blade info
                status = ec.status()
                print(f"[DEBUG] Engine status available: {bool(status)}")
                return []  # Return empty for now, at least we can test job submission
            except Exception as e2:
                print(f"[ERROR] Alternative queries also failed: {e2}")
                return []
        
        if not blades:
            print("[DEBUG] No blades returned from query")
            return []
            
        nuke_blades = []
        active_count = 0
        
        for blade in blades:
            name = blade.get('name', 'unknown')
            nimby = blade.get('nimby', 'unknown')
            profile = blade.get('profile', {})
            
            print(f"[DEBUG] Blade {name}: nimby={nimby}, profile keys={list(profile.keys())}")
            
            # Count active blades
            if nimby == 'off':
                active_count += 1
                
                services = profile.get('service', [])
                envkeys = profile.get('envkey', [])
                crews = profile.get('crews', [])
                
                if services:  # Only include blades with services
                    blade_entry = {
                        'name': name,
                        'services': services,
                        'envkeys': envkeys,
                        'crews': crews,
                        'nimby': nimby
                    }
                    nuke_blades.append(blade_entry)
        
        print(f"[DEBUG] Found {active_count} active blades, {len(nuke_blades)} with services")
        return nuke_blades
        
    except Exception as e:
        print(f"[ERROR] Failed to query blades: {e}")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return []

class SubmitToTractorUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SubmitToTractorUI, self).__init__(parent)
        self.setWindowTitle("Tractor Spool - Main")
        self.setMinimumWidth(450)  # Much thinner - reduced from 600
        self.setMaximumWidth(600)  # Prevent it from getting too wide
        self.setMinimumHeight(600)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Compact margins
        main_layout.setSpacing(10)  # Tighter spacing between sections

        # Header row with icon and title side-by-side
        header_layout = QtWidgets.QHBoxLayout()

        # Icon
        icon_path = os.path.join(os.path.dirname(__file__), "icon/tractorSpool.png")
        if os.path.exists(icon_path):
            icon_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(icon_path)
            pixmap = pixmap.scaledToHeight(48, QtCore.Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(QtCore.Qt.AlignVCenter)
            header_layout.addWidget(icon_label)
        else:
            print("[TractorSpool UI] Icon file not found:", icon_path)
        # Title
        header_label = QtWidgets.QLabel(tractorSpoolWindowTitle)
        header_font = header_label.font()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(QtCore.Qt.AlignVCenter)
        header_layout.addWidget(header_label)
        # Spacer to push title+icon left or center if needed
        header_layout.addStretch()
        # Add the full header row to the main layout
        main_layout.addLayout(header_layout)


        user_label = QtWidgets.QLabel(f"Logged in as: {getpass.getuser()}")
        user_label.setAlignment(QtCore.Qt.AlignRight)
        main_layout.addWidget(user_label)

        # Single column layout (no more left/right columns)
        # Write nodes section
        main_layout.addWidget(QtWidgets.QLabel("Write Nodes"))
        self.writeList = QtWidgets.QListWidget()
        self.writeList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        main_layout.addWidget(self.writeList)
        self.writeList.setMaximumHeight(150)  # Limit height instead of width
        
        # Buttons row
        buttons_layout = QtWidgets.QHBoxLayout()
        self.refreshWriteNodesButton = QtWidgets.QPushButton("Refresh Write Nodes")
        self.refreshWriteNodesButton.setMaximumWidth(160)  # Compact button
        self.refreshWriteNodesButton.clicked.connect(self.populateWriteNodes)
        buttons_layout.addWidget(self.refreshWriteNodesButton)
        
        # Submit button (moved from bottom)
        self.submitButton = QtWidgets.QPushButton("SPOOL JOB")
        self.submitButton.setMaximumWidth(120)  # Compact button
        self.submitButton.setStyleSheet("""
            QPushButton {
                background-color: darkGrey;
                color: black;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px 12px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #aa2222;
            }
        """)
        self.submitButton.clicked.connect(self.submitJobs)
        buttons_layout.addWidget(self.submitButton)
        
        buttons_layout.addStretch()  # Push buttons to the left
        main_layout.addLayout(buttons_layout)
        
        # Tractor Job Monitor below the buttons
        main_layout.addWidget(QtWidgets.QLabel(""))  # Spacer
        
        tractor_label = QtWidgets.QLabel("Tractor Job Monitor")
        tractor_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        main_layout.addWidget(tractor_label)
        
        # Clickable hyperlink to Tractor server
        self.tractorLink = QtWidgets.QLabel('<a href="http://10.31.240.8/tv/" style="color: #4A90E2; text-decoration: none; font-size: 12px;">🔗 Open Tractor Web Interface</a>')
        self.tractorLink.setOpenExternalLinks(True)
        self.tractorLink.setMaximumWidth(300)  # Limit width for compactness
        self.tractorLink.setStyleSheet("""
            QLabel {
                padding: 8px;
                border: 1px solid #4A90E2;
                border-radius: 5px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
            QLabel:hover {
                background-color: #e3f2fd;
                border-color: #2196F3;
            }
        """)
        self.tractorLink.setToolTip("Click to open Tractor job monitoring interface in web browser")
        main_layout.addWidget(self.tractorLink)
        
        # Add information text
        info_text = QtWidgets.QLabel("Monitor job status, logs, and farm activity through the Tractor web interface.")
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #666; font-size: 11px; margin-top: 10px;")
        main_layout.addWidget(info_text)
        
        # Spool Settings form
        main_layout.addWidget(QtWidgets.QLabel(""))  # Spacer
        form_label = QtWidgets.QLabel("Spool Settings")
        form_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        main_layout.addWidget(form_label)
        
        # Create a form layout for better organization
        form_widget = QtWidgets.QWidget()
        form_widget.setMaximumWidth(650)  # Limit form width
        form_layout = QtWidgets.QGridLayout(form_widget)
        form_layout.setSpacing(8)  # Tighter spacing
        form_layout.setContentsMargins(2, 2, 2, 2)  # Compact margins
        
        # Frame range (row 0)
        self.firstFrameField = QtWidgets.QSpinBox()
        self.lastFrameField = QtWidgets.QSpinBox()
        self.firstFrameField.setMaximum(999999)
        self.lastFrameField.setMaximum(999999)
        self.firstFrameField.setMaximumWidth(80)  # Compact width
        self.lastFrameField.setMaximumWidth(80)   # Compact width
        form_layout.addWidget(QtWidgets.QLabel("First Frame"), 0, 0)
        form_layout.addWidget(self.firstFrameField, 0, 1)
        form_layout.addWidget(QtWidgets.QLabel("Last Frame"), 0, 2)
        form_layout.addWidget(self.lastFrameField, 0, 3)

        # Project (row 1)
        self.projectField = QtWidgets.QComboBox()
        self.projectField.setEditable(True)
        self.projectField.setMaximumWidth(300)  # Limit width
        form_layout.addWidget(QtWidgets.QLabel("Project"), 1, 0)
        form_layout.addWidget(self.projectField, 1, 1, 1, 3)  # Span 3 columns

        # Priority (row 2)
        self.priorityField = QtWidgets.QSpinBox()
        self.priorityField.setMinimum(1)
        self.priorityField.setMaximum(999)
        self.priorityField.setValue(1)
        self.priorityField.setMaximumWidth(70)  # Compact width
        self.priorityField.setToolTip("Lower = higher priority")
        form_layout.addWidget(QtWidgets.QLabel("Priority"), 2, 0)
        form_layout.addWidget(self.priorityField, 2, 1)

        # Service dropdown (row 2 continued)
        self.serviceCombo = QtWidgets.QComboBox()
        self.serviceCombo.addItems(["PixarRender", "NukeXRender", "NukeRender", "Custom"])
        self.serviceCombo.setCurrentText("PixarRender")
        self.serviceCombo.setMaximumWidth(120)  # Compact width
        self.serviceCombo.setToolTip("Select the Tractor service - PixarRender is recommended for your farm")
        form_layout.addWidget(QtWidgets.QLabel("Service"), 2, 2)
        form_layout.addWidget(self.serviceCombo, 2, 3)
        
        # Custom service field (row 3)
        self.customServiceField = QtWidgets.QLineEdit()
        self.customServiceField.setPlaceholderText("Enter custom service name")
        self.customServiceField.setMaximumWidth(250)  # Limit width
        self.customServiceField.setVisible(False)
        form_layout.addWidget(self.customServiceField, 3, 1, 1, 3)  # Span 3 columns
        
        # Envkey field (row 4)
        self.envkeyField = QtWidgets.QLineEdit()
        self.envkeyField.setPlaceholderText("Leave empty for any environment")
        self.envkeyField.setMaximumWidth(150)  # Compact width
        self.envkeyField.setToolTip("Environment key for blade matching (leave empty to match any)")
        form_layout.addWidget(QtWidgets.QLabel("Envkey"), 4, 0)
        form_layout.addWidget(self.envkeyField, 4, 1)
        
        # Max Active Tasks field (row 4 continued)
        self.maxActiveField = QtWidgets.QSpinBox()
        self.maxActiveField.setRange(0, 999)
        self.maxActiveField.setValue(10)
        self.maxActiveField.setMaximumWidth(80)  # Compact width
        self.maxActiveField.setSpecialValueText("Unlimited")
        self.maxActiveField.setToolTip("Maximum number of tasks to run simultaneously (0 = unlimited)")
        form_layout.addWidget(QtWidgets.QLabel("Max Active Tasks"), 4, 2)
        form_layout.addWidget(self.maxActiveField, 4, 3)
        
        # Connect service combo to update envkey
        self.serviceCombo.currentTextChanged.connect(self.updateEnvkey)
        self.updateEnvkey()  # Set initial value

        # Tags (row 5)
        self.tagField = QtWidgets.QLineEdit()
        self.tagField.setPlaceholderText("e.g. urgent,daily")
        self.tagField.setMaximumWidth(300)  # Limit width
        self.tagField.setToolTip("Optional job tags for filtering")
        form_layout.addWidget(QtWidgets.QLabel("Tags"), 5, 0)
        form_layout.addWidget(self.tagField, 5, 1, 1, 3)  # Span 3 columns

        # Comments (row 6)
        self.commentField = QtWidgets.QTextEdit()
        self.commentField.setPlaceholderText("Add comments about this job (optional)")
        self.commentField.setFixedHeight(60)
        self.commentField.setMaximumWidth(400)  # Limit width
        form_layout.addWidget(QtWidgets.QLabel("Comments"), 6, 0)
        form_layout.addWidget(self.commentField, 6, 1, 1, 3)  # Span 3 columns
        
        # Add the form widget to the main layout
        main_layout.addWidget(form_widget)

        # Load defaults
        self.populateWriteNodes()
        self.populateFrameRange()
        self.populateProjects()

    def populateWriteNodes(self):
        """Find all Write nodes, including those inside Groups and Gizmos"""
        self.writeList.clear()
        write_nodes = self.find_all_write_nodes()
        
        for node_info in write_nodes:
            node = node_info['node']
            display_name = node_info['display_name']
            
            if not node['disable'].value():
                item = QtWidgets.QListWidgetItem(display_name)
                # Store the actual node reference in the item data for later use
                item.setData(QtCore.Qt.UserRole, node)
                self.writeList.addItem(item)
        
        print(f"[DEBUG] Found {len(write_nodes)} Write nodes (including inside Groups/Gizmos)")

    def find_all_write_nodes(self):
        """Recursively find all Write nodes in the script, including inside Groups and Gizmos"""
        write_nodes = []
        
        def search_in_group(group_node, parent_path=""):
            """Recursively search for Write nodes inside a group"""
            try:
                # Enter the group context
                group_node.begin()
                try:
                    for node in nuke.allNodes():
                        if node.Class() == 'Write':
                            # Create display name with parent group info
                            if parent_path:
                                display_name = f"{node.name()} ({parent_path} > {group_node.name()})"
                            else:
                                display_name = f"{node.name()} ({group_node.name()})"
                            
                            write_nodes.append({
                                'node': node,
                                'display_name': display_name,
                                'parent_group': group_node.name(),
                                'parent_path': parent_path
                            })
                        
                        # Recursively search inside nested Groups and Gizmos
                        elif node.Class() in ['Group', 'Gizmo']:
                            nested_path = f"{parent_path} > {group_node.name()}" if parent_path else group_node.name()
                            search_in_group(node, nested_path)
                finally:
                    # Always exit the group context
                    group_node.end()
            except Exception as e:
                print(f"[WARNING] Error searching in group '{group_node.name()}': {e}")
        
        try:
            # First, find all Write nodes at root level
            for node in nuke.allNodes('Write'):
                write_nodes.append({
                    'node': node,
                    'display_name': node.name(),
                    'parent_group': None,
                    'parent_path': None
                })
            
            # Then search inside all Groups and Gizmos at root level
            for node in nuke.allNodes():
                if node.Class() in ['Group', 'Gizmo']:
                    search_in_group(node)
        except Exception as e:
            print(f"[ERROR] Error during Write node search: {e}")
        
        return write_nodes

    def populateFrameRange(self):
        self.firstFrameField.setValue(int(nuke.root()['first_frame'].value()))
        self.lastFrameField.setValue(int(nuke.root()['last_frame'].value()))

    def populateProjects(self):
        # Option 1: Look in ~/.nuke/tractor/
        project_file = os.path.join(os.path.expanduser("~/.nuke/tractor"), "live_projects.json")
        print(f"[Tractor UI] -Opt1- Looking for project file at: {project_file}")

        # Option 2 fallback: Look relative to the script
        if not os.path.exists(project_file):
            project_file = os.path.join(os.path.dirname(__file__), "live_projects.json")
            print(f"[Tractor UI] -Opt2- Looking for project file at: {project_file}")
        
        # Try to load from JSON file
        projects_loaded = False
        if os.path.exists(project_file):
            try:
                import json
                with open(project_file, 'r') as f:
                    projects = json.load(f)
                self.projectField.addItems(projects)
                projects_loaded = True
                print(f"[Tractor UI] Loaded {len(projects)} projects from {project_file}")
            except Exception as e:
                print(f"[Tractor UI] Failed to load project list: {e}")
        
        # Fallback: Auto-detect project from current script path
        if not projects_loaded:
            print(f"[Tractor UI] No project file found, attempting auto-detection...")
            try:
                script_path = nuke.root().name()
                if script_path and script_path != "Root":
                    detected_project = self.autoDetectProject(script_path)
                    if detected_project:
                        self.projectField.addItem(detected_project)
                        print(f"[Tractor UI] Auto-detected project: {detected_project}")
                    else:
                        # Add some common project names as fallback
                        common_projects = ["EXIT", "3D2", "3D3", "COMP", "RENDER"]
                        self.projectField.addItems(common_projects)
                        print(f"[Tractor UI] Added default project list")
                else:
                    # Add default projects if no script is loaded
                    default_projects = ["EXIT", "3D2", "3D3", "COMP", "RENDER"]
                    self.projectField.addItems(default_projects)
                    print(f"[Tractor UI] Added default project list (no script loaded)")
            except Exception as e:
                print(f"[Tractor UI] Auto-detection failed: {e}")
                # Final fallback
                self.projectField.addItem("EXIT")
    
    def autoDetectProject(self, script_path):
        """Auto-detect project name from script path"""
        try:
            # Import the folder detection from shotstudio
            import sys
            shotstudio_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\shotmanager"
            if shotstudio_path not in sys.path:
                sys.path.append(shotstudio_path)
            
            from shotstudio import detect_project_from_path
            project = detect_project_from_path(script_path)
            return project
            
        except Exception as e:
            print(f"[Tractor UI] Could not import shotstudio for project detection: {e}")
            
            # Simple fallback detection
            path_parts = script_path.replace('\\', '/').split('/')
            for part in path_parts:
                if part.upper() in ['3D2', '3D3', 'COMP', 'EXIT', 'RENDER']:
                    return part.upper()
            
            # Look for common project patterns
            for part in path_parts:
                if '_' in part and len(part) <= 10:  # Likely project code
                    return part.upper()
            
            return None

    def updateEnvkey(self):
        """Update envkey field based on selected service"""
        service = self.serviceCombo.currentText()
        
        # Keep envkey empty by default for maximum blade compatibility
        if service == "PixarRender":
            self.envkeyField.setText("")  # Empty for flexibility
            self.customServiceField.setVisible(False)
        elif service == "NukeXRender":
            self.envkeyField.setText("")  # Empty for flexibility
            self.customServiceField.setVisible(False)
        elif service == "NukeRender":
            self.envkeyField.setText("")  # Empty for flexibility
            self.customServiceField.setVisible(False)
        elif service == "Custom":
            self.envkeyField.setText("")
            self.customServiceField.setVisible(True)
        else:
            self.customServiceField.setVisible(False)

    def populateProjects(self):
        # Option 1: Look in ~/.nuke/tractor/
        project_file = os.path.join(os.path.expanduser("~/.nuke/tractor"), "live_projects.json")
        print(f"[Tractor UI] -Opt1- Looking for project file at: {project_file}")

        # Option 2 fallback: Look relative to the script
        if not os.path.exists(project_file):
            project_file = os.path.join(os.path.dirname(__file__), "live_projects.json")
            print(f"[Tractor UI] -Opt2- Looking for project file at: {project_file}")
        
        # Try to load from JSON file
        projects_loaded = False
        if os.path.exists(project_file):
            try:
                import json
                with open(project_file, 'r') as f:
                    projects = json.load(f)
                self.projectField.addItems(projects)
            except Exception as e:
                print(f"[Tractor UI] Failed to load project list: {e}")


    def replace_connect_nodes(self, connect_nodes):
        """Replace Connect.gizmo nodes with Dot nodes to fix render compatibility"""
        replaced_count = 0
        
        for connect_node in connect_nodes:
            try:
                print(f"[DEBUG] Replacing {connect_node.name()}")
                
                # Get input connection
                input_node = connect_node.input(0) if connect_node.inputs() > 0 else None
                
                # Get all nodes that depend on this connect node
                output_nodes = connect_node.dependent()
                
                # Create a Dot node to replace the Connect
                dot = nuke.createNode('Dot', inpanel=False)
                dot.setName(f"Dot_{connect_node.name().replace('.', '_')}")
                
                # Set position near the original node
                if hasattr(connect_node, 'xpos') and hasattr(connect_node, 'ypos'):
                    dot.setXYpos(connect_node.xpos(), connect_node.ypos())
                
                # Connect the input
                if input_node:
                    dot.setInput(0, input_node)
                
                # Reconnect all outputs
                for output_node in output_nodes:
                    for i in range(output_node.inputs()):
                        if output_node.input(i) == connect_node:
                            output_node.setInput(i, dot)
                
                # Delete the original Connect node
                nuke.delete(connect_node)
                replaced_count += 1
                
            except Exception as e:
                print(f"[ERROR] Failed to replace {connect_node.name()}: {e}")
        
        # Save the script if replacements were made
        if replaced_count > 0:
            try:
                nuke.scriptSave()
                print(f"[DEBUG] Script saved with {replaced_count} Connect node replacements")
            except Exception as e:
                print(f"[ERROR] Failed to save script: {e}")
        
        return replaced_count

    def is_absolute_path(self, path):
        r"""
        Enhanced path detection that handles various absolute path formats:
        - Windows: C:\path\to\file
        - UNC: \\server\share\path or //server/share/path  
        - Unix: /path/to/file
        - Network with drive: Z:\path\to\file
        """
        if not path or not isinstance(path, str):
            return False
        
        path = path.strip()
        if not path:
            return False
        
        # Use os.path.isabs as the primary check
        if os.path.isabs(path):
            return True
        
        # Additional checks for UNC paths that might not be caught
        # UNC paths: \\server\share or //server/share
        if path.startswith('\\\\') or path.startswith('//'):
            return True
        
        # Check for drive letters (Windows)
        if len(path) >= 3 and path[1] == ':' and path[0].isalpha():
            return True
        
        return False
    
    def normalize_path_for_farm(self, path):
        """
        Normalize a path for render farm compatibility.
        Converts to forward slashes and ensures proper UNC format.
        """
        if not path:
            return path
        
        # Normalize path separators
        normalized = path.replace('\\', '/')
        
        # Ensure UNC paths start with // (not \\)
        if normalized.startswith('\\\\'):
            normalized = '//' + normalized[2:]
        
        return normalized
    
    def has_dynamic_expressions(self, path):
        """
        Check if path contains TCL expressions or environment variables 
        that should be resolved at render time rather than being converted.
        """
        if not path or not isinstance(path, str):
            return False
        
        # TCL expression indicators
        tcl_indicators = [
            '[',              # TCL expression brackets [file dirname ...]
            '${',             # Unix environment variables ${VAR}
            '$env(',          # TCL environment variables $env(VAR)
            '[getenv',        # TCL getenv function
            '[python',        # Python expressions in TCL
            '[value root',    # Common Nuke script references
            '[file ',         # TCL file operations
        ]
        
        # Windows environment variables %VAR%
        if '%' in path and path.count('%') >= 2:
            return True
        
        # Unix environment variables starting with $ (but not just $)
        if path.startswith('$') and len(path) > 1 and path[1].isalpha():
            return True
        
        # Check for TCL indicators
        for indicator in tcl_indicators:
            if indicator in path:
                return True
        
        return False
    
    def get_path_info(self, path):
        """
        Get detailed information about a path for debugging.
        """
        if not path:
            return "Empty path"
        
        info = []
        info.append(f"Path: '{path}'")
        info.append(f"os.path.isabs(): {os.path.isabs(path)}")
        info.append(f"is_absolute_path(): {self.is_absolute_path(path)}")
        info.append(f"has_dynamic_expressions(): {self.has_dynamic_expressions(path)}")
        
        if path.startswith('\\\\') or path.startswith('//'):
            info.append("Type: UNC path")
        elif len(path) >= 3 and path[1] == ':' and path[0].isalpha():
            info.append("Type: Windows drive path")
        elif path.startswith('/'):
            info.append("Type: Unix-style absolute path")
        elif self.has_dynamic_expressions(path):
            info.append("Type: Dynamic expression")
        else:
            info.append("Type: Relative path")
        
        return " | ".join(info)

    def submitJobs(self):
        """Submit jobs to Tractor render farm"""
        tq.setEngineClientParam(user=SIMTRACKER["user"], password=SIMTRACKER["password"])
        
        selected_items = self.writeList.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select at least one Write node.")
            return

        script_path = nuke.root().name()
        if script_path == "Root":
            QtWidgets.QMessageBox.warning(self, "Unsaved Script", "Please save your script before submitting to Tractor.")
            return
            
        # Check for Connect.gizmo nodes that might cause render failures
        connect_nodes = []
        for node in nuke.allNodes():
            if 'Connect' in node.name() and ('gizmo' in node.Class().lower() or node.Class() == 'Group'):
                connect_nodes.append(node)
        
        if connect_nodes:
            msg = f"Found {len(connect_nodes)} Connect.gizmo nodes that may cause render failures:\n"
            for node in connect_nodes[:5]:  # Show first 5
                msg += f"- {node.name()}\n"
            if len(connect_nodes) > 5:
                msg += f"... and {len(connect_nodes) - 5} more\n"
            msg += "\nThese nodes are known to cause 'unknown command' errors on render blades.\n"
            msg += "Would you like to automatically replace them with Dot nodes before submitting?"
            
            response = QtWidgets.QMessageBox.question(self, "Connect.gizmo Detected", msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            
            if response == QtWidgets.QMessageBox.Cancel:
                return
            elif response == QtWidgets.QMessageBox.Yes:
                # Replace Connect nodes with Dots
                replaced_count = self.replace_connect_nodes(connect_nodes)
                if replaced_count > 0:
                    QtWidgets.QMessageBox.information(self, "Nodes Replaced", 
                        f"Successfully replaced {replaced_count} Connect nodes with Dot nodes.\n"
                        "The script has been saved. Proceeding with job submission.")
                else:
                    QtWidgets.QMessageBox.warning(self, "Replacement Failed", 
                        "Failed to replace Connect nodes. Please fix manually before submitting.")
                    return

        first_frame = self.firstFrameField.value()
        last_frame = self.lastFrameField.value()
        project_name = self.projectField.currentText()
        priority = self.priorityField.value()
        service = self.serviceCombo.currentText()
        if service == "Custom":
            service = self.customServiceField.text().strip()
            if not service:
                QtWidgets.QMessageBox.warning(self, "Invalid Service", "Please enter a custom service name.")
                return
        elif service == "None (Default)":
            service = ""  # Empty service for maximum compatibility
        
        # Validate that service is set - your farm requires a specific service
        if not service:
            QtWidgets.QMessageBox.warning(self, "No Service", "Please select a service. PixarRender is recommended for your farm.")
            return
        
        # Get envkey from field (keep empty if not specified)
        envkey = self.envkeyField.text().strip()
        
        # Get max active from field
        maxactive = self.maxActiveField.value()
        
        tags = [t.strip() for t in self.tagField.text().split(",") if t.strip()]
        comments = self.commentField.toPlainText().strip()
        spoolfile = script_path  # Use the script path as the spool file

        # Store original Write node paths for restoration after job submission
        original_write_paths = {}
        for item in selected_items:
            # Get the actual node from stored data, not from text
            write_node = item.data(QtCore.Qt.UserRole)
            if write_node and 'file' in write_node.knobs():
                original_write_paths[write_node.name()] = write_node['file'].value()

        errors = 0
        submitted_jobs = []  # Store job IDs and titles for confirmation dialog
        for item in selected_items:
            # Get the actual node from stored data
            write_node = item.data(QtCore.Qt.UserRole)
            display_name = item.text()  # For display purposes
            write_name = write_node.name() if write_node else None
            
            # Validate that the Write node exists
            if write_node is None:
                QtWidgets.QMessageBox.warning(self, "Write Node Error", f"Write node from '{display_name}' not found.")
                continue
                
            # Validate that the Write node has a proper file path
            try:
                # Check both 'file' knob and potential relative path knobs
                file_path = ""
                if 'file' in write_node.knobs():
                    file_path = write_node['file'].value()
                
                print(f"[DEBUG] {write_name} ({display_name}) initial path info: {self.get_path_info(file_path)}")
                
                # If file path is empty or relative, try to get the full path
                if not file_path or not self.is_absolute_path(file_path):
                    # Try to get the evaluated/full path
                    try:
                        # Use Nuke's filename() method to get the evaluated path
                        evaluated_path = write_node.filename()
                        if evaluated_path and self.is_absolute_path(evaluated_path):
                            file_path = evaluated_path
                            print(f"[DEBUG] {write_name} evaluated path: {self.get_path_info(file_path)}")
                    except Exception as eval_e:
                        print(f"[DEBUG] Could not evaluate path for {write_name}: {eval_e}")
                
                # If still relative, try to build absolute path based on script location
                if file_path and not self.is_absolute_path(file_path):
                    script_dir = os.path.dirname(script_path)
                    potential_abs_path = os.path.join(script_dir, file_path)
                    potential_abs_path = os.path.normpath(potential_abs_path)
                    
                    # Normalize for farm compatibility
                    potential_abs_path = self.normalize_path_for_farm(potential_abs_path)
                    
                    print(f"[DEBUG] Converted relative path '{file_path}' to absolute: '{potential_abs_path}'")
                    print(f"[DEBUG] Final path info: {self.get_path_info(potential_abs_path)}")
                    
                    # Update the write node with the absolute path for render
                    try:
                        write_node['file'].setValue(potential_abs_path)
                        file_path = potential_abs_path
                        print(f"[DEBUG] Updated Write node '{write_name}' with absolute path")
                    except Exception as update_e:
                        print(f"[WARNING] Could not update write node path: {update_e}")
                        # Continue with the original path and warn user
                        pass
                else:
                    # Path is already absolute, just normalize for farm compatibility
                    if self.is_absolute_path(file_path):
                        normalized_path = self.normalize_path_for_farm(file_path)
                        if normalized_path != file_path:
                            print(f"[DEBUG] Normalizing absolute path for farm compatibility:")
                            print(f"[DEBUG] Original: {file_path}")
                            print(f"[DEBUG] Normalized: {normalized_path}")
                            try:
                                write_node['file'].setValue(normalized_path)
                                file_path = normalized_path
                            except Exception as norm_e:
                                print(f"[WARNING] Could not normalize path: {norm_e}")
                        else:
                            print(f"[DEBUG] Absolute path already properly formatted: {file_path}")
                
                # Final validation and auto-fix for empty paths
                if not file_path or file_path.strip() == "":
                    print(f"[DEBUG] Write node '{write_name}' has no file path - attempting auto-fix...")
                    
                    # Auto-generate a suitable file path
                    script_dir = os.path.dirname(script_path)
                    script_name = os.path.splitext(os.path.basename(script_path))[0]
                    
                    # Create renders subdirectory path only if no path exists
                    auto_filename = f"{script_name}_{write_name}.####.exr"
                    auto_path = os.path.join(script_dir, "renders", auto_filename)
                    auto_path = auto_path.replace("\\", "/")
                    
                    # Set the auto-generated path
                    try:
                        write_node['file'].setValue(auto_path)
                        file_path = auto_path
                        print(f"[DEBUG] Auto-fixed Write node '{write_name}' with path: {auto_path}")
                        
                        # Create renders directory if it doesn't exist
                        renders_dir = os.path.join(script_dir, "renders")
                        if not os.path.exists(renders_dir):
                            os.makedirs(renders_dir)
                            print(f"[DEBUG] Created renders directory: {renders_dir}")
                            
                        # Save the script with the updated path
                        nuke.scriptSave()
                        print(f"[DEBUG] Saved script with updated Write node path")
                        
                    except Exception as fix_e:
                        print(f"[ERROR] Could not auto-fix Write node '{write_name}': {fix_e}")
                        QtWidgets.QMessageBox.warning(self, "Missing Output Path", 
                            f"Write node '{write_name}' has no output file path specified.\n"
                            "Auto-fix failed. Please set a file path manually in the Write node.")
                        continue
                
                # Double-check the file path after potential auto-fix
                try:
                    current_file_path = write_node['file'].value()
                    if not current_file_path or current_file_path.strip() == "":
                        QtWidgets.QMessageBox.critical(self, "Write Node Error", 
                            f"Write node '{write_name}' still has no output file path after auto-fix attempt.\n"
                            "Please manually set a valid file path in the Write node before submitting.")
                        continue
                    file_path = current_file_path
                    print(f"[DEBUG] Write node '{write_name}' using existing file path: {file_path}")
                except Exception as check_e:
                    print(f"[ERROR] Could not verify Write node path: {check_e}")
                    continue
                
                # Check if it contains TCL expressions or environment variables
                if file_path and not self.is_absolute_path(file_path):
                    # Check if it contains dynamic expressions that should be resolved at render time
                    if self.has_dynamic_expressions(file_path):
                        print(f"[DEBUG] Write node '{write_name}' uses dynamic expressions: {file_path}")
                        print(f"[DEBUG] This will be resolved by Nuke during render - no conversion needed")
                    else:
                        print(f"[DEBUG] Write node '{write_name}' has simple relative path: {file_path}")
                        print(f"[DEBUG] Will show warning but allow submission")
                        QtWidgets.QMessageBox.warning(self, "Relative Path Warning", 
                            f"Write node '{write_name}' has a relative path: {file_path}\n"
                            "Consider using absolute network paths for better render farm compatibility.\n"
                            "The system will attempt to resolve this automatically.")
                else:
                    print(f"[DEBUG] Write node '{write_name}' has absolute path: {file_path}")
                    print(f"[DEBUG] Path details: {self.get_path_info(file_path)}")
                
                # Additional check for Write node format compatibility
                try:
                    file_type = write_node['file_type'].value()
                    print(f"[DEBUG] Write node '{write_name}' format: {file_type}")
                    
                    # Check for problematic formats
                    if file_type.lower() in ['mov', 'mp4', 'avi']:
                        response = QtWidgets.QMessageBox.question(self, "Video Format Warning", 
                            f"Write node '{write_name}' uses video format '{file_type}' which may not be suitable for frame-by-frame rendering.\n"
                            "Video formats often require all frames to be processed together.\n"
                            "Consider changing to an image sequence format (EXR, TIFF, PNG).\n\n"
                            "Do you want to continue anyway?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                        if response == QtWidgets.QMessageBox.No:
                            continue
                            
                    # Check if Write node has frame range restrictions
                    if hasattr(write_node, 'first') and hasattr(write_node, 'last'):
                        write_first = write_node['first'].value()
                        write_last = write_node['last'].value()
                        if write_first == write_last:
                            print(f"[WARNING] Write node '{write_name}' is set to render only frame {write_first}")
                            
                except Exception as format_e:
                    print(f"[WARNING] Could not check format for Write node '{write_name}': {format_e}")
                
                print(f"[DEBUG] Write node '{write_name}' file path: {file_path}")
                
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Write Node Validation Error", 
                    f"Error validating Write node '{write_name}': {str(e)}")
                continue
            
            title = f"[{project_name}] {os.path.basename(script_path)} - {write_name}"

            job = Job()
            job.title = title
            job.priority = priority

            # Keep projects as array for multiple project selection
            if project_name:
                job.projects = [project_name]
            
            # Set job-level service (critical for blade matching)
            if service:
                job.service = service
                print(f"[DEBUG] Setting job service to: '{service}'")
            else:
                # When service is empty, don't set it at all for maximum compatibility
                print(f"[DEBUG] Using empty service for maximum blade compatibility")
                # Don't set job.service at all - let it remain undefined
            
            if tags:
                job.tags = tags
            if comments:
                job.comment = comments
            
            # Don't force crews - let it be empty for maximum compatibility
            # job.crews = ['3D4']  # This was forcing a specific crew requirement
            print(f"[DEBUG] Using empty crews for maximum blade compatibility")
            
            # Set job-level environment requirements (critical for blade matching)
            if envkey:
                job.envkey = [envkey]
                print(f"[DEBUG] Setting job envkey to: {envkey}")
            else:
                # Empty envkey for maximum compatibility (like working example)
                job.envkey = []
                print(f"[DEBUG] Using empty envkey for maximum blade compatibility")
            
            # Set max active tasks from UI field
            job.maxactive = maxactive
            
            # Add serialsubtasks (controls task execution order)
            # 1 = tasks must run in order, 0 = tasks can run in parallel
            job.serialsubtasks = 1  # Keep ordered execution for now

            # Create master task for this write node
            master_task = Task(title=f"Render {write_name}")
            master_task.serialsubtasks = 0  # Allow parallel frame execution
            
            print(f"[DEBUG] Created master task, checking children attribute...")
            print(f"[DEBUG] Master task children type: {type(getattr(master_task, 'children', None))}")
            
            # Add one subtask per frame
            for frame_idx, frame in enumerate(range(first_frame, last_frame + 1)):
                # Use full path to Nuke executable for better blade compatibility
                nuke_exe = r"C:\Program Files\Nuke15.1v2\Nuke15.1.exe"
                if not os.path.exists(nuke_exe):
                    # Fallback to just "nuke.exe" if full path doesn't exist
                    nuke_exe = "nuke.exe"
                
                # Build command for render farm using temporary Python script approach
                # Create a temporary Python script file for reliable execution
                import tempfile
                import time
                
                # Generate timestamp for the script
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Create temporary Python script for this frame
                python_content = f'''#!/usr/bin/env python
"""
Tractor Nuke Render Script
Generated: {current_time}
Script: {os.path.basename(script_path)}
Write Node: {write_name}
Frame: {frame}
"""

import nuke
import sys
import os

try:
    # Open the Nuke script
    script_path = r"{script_path}"
    print("=" * 60)
    print("TRACTOR NUKE RENDER - Frame {frame}")
    print("=" * 60)
    print("Script: %s" % script_path)
    print("Write Node: {write_name}")
    print("Frame: {frame}")
    print("Timestamp: {current_time}")
    print("=" * 60)
    
    print("Opening Nuke script...")
    nuke.scriptOpen(script_path)
    print("Script opened successfully")
    
    # Find the Write node
    write_name = "{write_name}"
    write_node = nuke.toNode(write_name)
    
    if not write_node:
        print("ERROR: Write node '%s' not found in script" % write_name)
        available_writes = [n.name() for n in nuke.allNodes("Write")]
        print("Available Write nodes: %s" % available_writes)
        sys.exit(1)
    
    print("Write node found: %s" % write_node)
    
    # Get the original file path
    original_path = write_node['file'].value()
    print("Original file path: %s" % original_path)
    
    if not original_path or original_path.strip() == "":
        print("ERROR: Write node '%s' has no output file path" % write_name)
        sys.exit(1)
    
    # Set current frame and calculate final path
    frame = {frame}
    nuke.frame(frame)
    print("Current frame set to: %d" % frame)
    
    # Manual frame substitution (most reliable method)
    import re
    if '%04d' in original_path:
        final_path = original_path.replace('%04d', '%04d' % frame)
    elif '####' in original_path:
        final_path = original_path.replace('####', '%04d' % frame)
    else:
        final_path = original_path
    
    print("Final output path: %s" % final_path)
    
    # Check if the directory exists and create if needed
    output_dir = os.path.dirname(final_path)
    if not os.path.exists(output_dir):
        print("Creating output directory: %s" % output_dir)
        try:
            os.makedirs(output_dir)
            print("Directory created successfully")
        except Exception as dir_e:
            print("ERROR creating directory: %s" % dir_e)
            sys.exit(1)
    else:
        print("Output directory exists: %s" % output_dir)
    
    # Set the file path to the frame-specific path
    original_file_path = write_node['file'].value()  # Save original path
    write_node['file'].setValue(final_path)
    print("Set Write node file path to: %s" % final_path)
    
    # Execute the Write node for the specific frame
    print("=" * 60)
    print("STARTING RENDER...")
    print("=" * 60)
    import time
    start_time = time.time()
    
    nuke.execute(write_node, frame, frame)
    
    end_time = time.time()
    render_duration = end_time - start_time
    print("=" * 60)
    print("RENDER COMPLETED SUCCESSFULLY!")
    print("Render time: %.2f seconds" % render_duration)
    print("=" * 60)
    
    # Restore original file path
    write_node['file'].setValue(original_file_path)
    print("Restored original file path: %s" % original_file_path)
    
    # Save the script to preserve the original path
    nuke.scriptSave()
    print("Saved script with restored original path")
    
    # Verify the output file was created
    if os.path.exists(final_path):
        file_size = os.path.getsize(final_path)
        print("SUCCESS: Output file created")
        print("  File: %s" % final_path)
        print("  Size: %d bytes (%.2f MB)" % (file_size, file_size / 1024.0 / 1024.0))
        
        # Clean up this render script on success
        try:
            current_script = __file__ if '__file__' in globals() else None
            if current_script and os.path.exists(current_script):
                os.remove(current_script)
                print("Cleaned up render script: %s" % current_script)
        except:
            pass  # Don't fail if cleanup fails
            
    else:
        print("WARNING: Could not find output file: %s" % final_path)
        # List files in the directory to see what was actually created
        try:
            files = [f for f in os.listdir(output_dir) if f.endswith('.exr')]
            if files:
                print("EXR files in output directory: %s" % files)
            else:
                print("No EXR files found in output directory")
        except:
            print("Could not list files in output directory")
    
except Exception as e:
    print("=" * 60)
    print("ERROR DURING RENDER")
    print("=" * 60)
    print("ERROR: %s" % str(e))
    import traceback
    traceback.print_exc()
    print("=" * 60)
    sys.exit(1)
'''
                
                # Create organized directory structure for Python render scripts
                script_dir = os.path.dirname(script_path)
                script_name = os.path.splitext(os.path.basename(script_path))[0]  # Get script name without extension
                
                # Create py/<script_name>/ folder structure
                py_scripts_dir = os.path.join(script_dir, "py", script_name)
                
                # Ensure the directory exists
                try:
                    if not os.path.exists(py_scripts_dir):
                        os.makedirs(py_scripts_dir)
                        print(f"[DEBUG] Created Python scripts directory: {py_scripts_dir}")
                except Exception as dir_e:
                    print(f"[WARNING] Could not create Python scripts directory: {dir_e}")
                    # Fallback to script directory
                    py_scripts_dir = script_dir
                
                # Generate Python script filename with timestamp for uniqueness
                timestamp = int(time.time())
                temp_py_file = os.path.join(py_scripts_dir, f"render_{write_name}_f{frame}_{timestamp}.py")
                
                try:
                    with open(temp_py_file, 'w') as f:
                        f.write(python_content)
                    print(f"[DEBUG] Created temporary Python script: {temp_py_file}")
                    
                    cmd = [
                        nuke_exe, 
                        "-t",  # Use headless mode for better farm compatibility
                        temp_py_file  # Execute the Python script
                    ]
                    
                except Exception as py_e:
                    print(f"[ERROR] Could not create Python script: {py_e}")
                    # Fallback to original approach
                    cmd = [
                        nuke_exe, 
                        "-x", script_path,
                        "-F", f"{frame}-{frame}",
                        "-X", write_name
                    ]
                
                print(f"[DEBUG] Frame {frame} command: {' '.join(cmd)}")
                
                # Create frame task with proper environment variables
                frame_task = Task(title=f"Frame {frame}", argv=cmd)
                frame_task.id = f"id{frame_idx+1:04d}"  # Add task ID
                
                # Set environment variables for the task - This is critical for plugin loading
                nuke_plugin_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke"
                env_vars = {
                    'NUKE_PATH': nuke_plugin_path,
                    'PYTHONPATH': nuke_plugin_path,  # Also set Python path for custom Python modules
                }
                
                # Try different ways to set environment variables based on Tractor API version
                try:
                    if hasattr(frame_task, 'envvars'):
                        frame_task.envvars = env_vars
                        print(f"[DEBUG] Set environment via envvars: {env_vars}")
                    elif hasattr(frame_task, 'env'):
                        frame_task.env = env_vars 
                        print(f"[DEBUG] Set environment via env: {env_vars}")
                    else:
                        # Fallback: try to set via serializing
                        print(f"[DEBUG] Task object does not support environment variables directly")
                        print(f"[DEBUG] Will rely on system NUKE_PATH: {nuke_plugin_path}")
                except Exception as env_e:
                    print(f"[WARNING] Could not set environment variables: {env_e}")
                    print(f"[DEBUG] Will rely on system NUKE_PATH: {nuke_plugin_path}")
                
                # Note: service, envkey, refersto are Job-level attributes only in Tractor API
                # Task-level attributes in ALF are handled differently vs Python API
                
                print(f"[DEBUG] Adding frame task {frame} to master task...")
                master_task.addChild(frame_task)
                
            print(f"[DEBUG] After adding children, master_task.children type: {type(getattr(master_task, 'children', None))}")
            children = getattr(master_task, 'children', None)
            children_count = len(children) if children is not None else 0
            print(f"[DEBUG] Children count: {children_count}")

            # Add master task to the job
            job.addChild(master_task)

            # Debug: Print job structure before spooling
            print(f"[DEBUG] Job TCL for {write_name}:")
            print(job.asTcl())
            print("=" * 50)
            
            # Debug: Print job attributes that are critical for blade matching
            print(f"[DEBUG] Job attributes (Nuke-specific structure):")
            print(f"  Service: {getattr(job, 'service', 'None')}")
            print(f"  Envkey: {getattr(job, 'envkey', 'None')}")
            print(f"  Crews: {getattr(job, 'crews', 'None')}")
            print(f"  Projects: {getattr(job, 'projects', 'None')}")
            print(f"  MaxActive: {getattr(job, 'maxactive', 'None')}")
            print(f"  SerialSubtasks: {getattr(job, 'serialsubtasks', 'None')}")
            
            # Handle master_task.children safely
            task_children = getattr(master_task, 'children', None)
            if task_children:
                print(f"[DEBUG] Master task has {len(task_children)} frame subtasks")
                sample_task = task_children[0]
                print(f"[DEBUG] Sample frame task attributes:")
                print(f"  ID: {getattr(sample_task, 'id', 'None')}")
                print(f"  Title: {getattr(sample_task, 'title', 'None')}")
                print(f"  Args: {getattr(sample_task, 'argv', 'None')}")
                print(f"  Note: service/envkey/refersto are ALF-only, not in Python API")
            else:
                print(f"[DEBUG] Master task has no children or children is None")
            print("=" * 50)

            try:
                result = spool_job_via_bridge(job.asTcl(), filename=script_path)
                print(f"[DEBUG] Raw spool result type: {type(result)}")
                print(f"[DEBUG] Raw spool result repr: {repr(result)}")
                print(f"[DEBUG] Raw spool result: {result}")
                
                # Check if result is actually a valid job ID
                if result == 0 or result == '0' or result is None:
                    print(f"[ERROR] Invalid job ID returned: {result}")
                    print(f"[ERROR] This usually indicates a Tractor submission failure")
                    # You might want to check the Tractor engine logs for errors
                    QtWidgets.QMessageBox.critical(self, "Submission Failed", 
                        f"Job submission failed for Write node '{write_name}'.\n"
                        f"Tractor returned job ID: {result}\n\n"
                        "This usually indicates:\n"
                        "• Tractor engine is not running\n"
                        "• Network connectivity issues\n"
                        "• Job validation errors\n\n"
                        "Check the Tractor engine logs for more details.")
                    errors += 1
                    continue
                
                print(f"[DEBUG] Job submitted successfully with ID: {result}")
                
                # Clean and validate job ID more thoroughly
                job_id = str(result).strip()
                print(f"[DEBUG] Raw job ID from spool: '{job_id}'")
                
                # Handle different result formats from Tractor
                actual_job_id = None
                
                # Check if result is a JSON string (new format)
                if job_id.startswith('{') and 'jid' in job_id:
                    try:
                        result_json = json.loads(job_id)
                        if 'jid' in result_json:
                            actual_job_id = str(result_json['jid'])
                            print(f"[DEBUG] Extracted job ID from JSON: {actual_job_id}")
                        elif 'msg' in result_json and 'jid:' in result_json['msg']:
                            # Extract from message like "job script accepted, jid: 21545"
                            import re
                            match = re.search(r'jid:\s*(\d+)', result_json['msg'])
                            if match:
                                actual_job_id = match.group(1)
                                print(f"[DEBUG] Extracted job ID from message: {actual_job_id}")
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"[WARNING] Failed to parse JSON result: {e}")
                
                # If JSON parsing failed, try regex extraction on the raw string
                if actual_job_id is None:
                    import re
                    # Look for patterns like {jid:12345}, jid:12345, or just numbers
                    jid_pattern = re.search(r'(?:jid[:=]\s*)?(\d+)', job_id)
                    if jid_pattern:
                        actual_job_id = jid_pattern.group(1)
                        print(f"[DEBUG] Extracted job ID via regex: {actual_job_id}")
                    else:
                        # Final fallback - extract any numeric sequence
                        numeric_match = re.search(r'\d+', job_id)
                        if numeric_match:
                            actual_job_id = numeric_match.group()
                            print(f"[DEBUG] Fallback job ID extraction: {actual_job_id}")
                
                # Use the extracted job ID
                if actual_job_id:
                    clean_job_id = actual_job_id
                    print(f"[DEBUG] Final clean job ID: {clean_job_id}")
                else:
                    # Use the original if extraction failed
                    clean_job_id = job_id
                    print(f"[WARNING] Could not extract numeric job ID, using raw: {clean_job_id}")
                
                # Final validation of job ID
                if clean_job_id == '0' or not clean_job_id:
                    print(f"[ERROR] Final job ID validation failed: '{clean_job_id}'")
                    QtWidgets.QMessageBox.critical(self, "Invalid Job ID", 
                        f"Invalid job ID returned for Write node '{write_name}': '{clean_job_id}'\n\n"
                        "The job may not have been submitted correctly.")
                    errors += 1
                    continue
                
                job_id = clean_job_id
                
                # Store job info for confirmation dialog
                submitted_jobs.append({
                    'id': job_id,
                    'title': title,
                    'write_node': write_name
                })
                
                # Try to get blade info after submission to compare with job requirements
                print("[DEBUG] Querying available blades for job matching analysis...")
                blade_info = get_blade_info()
                if blade_info:
                    print(f"[DEBUG] Found {len(blade_info)} blades with services:")
                    
                    # Check for exact matches
                    job_service = getattr(job, 'service', 'None')
                    job_envkey = getattr(job, 'envkey', [])
                    job_crews = getattr(job, 'crews', [])
                    
                    compatible_blades = []
                    for blade in blade_info:
                        blade_services = blade['services']
                        blade_envkeys = blade['envkeys']
                        blade_crews = blade['crews']
                        
                        # Check service compatibility
                        service_match = job_service in blade_services if job_service != 'None' else False
                        
                        # Check envkey compatibility (empty job envkey should match any blade)
                        envkey_match = (not job_envkey or  # Empty job envkey matches anything
                                      any(env in blade_envkeys for env in job_envkey))
                        
                        # Check crews compatibility (empty blade crews or matching crews)
                        crews_match = (not blade_crews or  # Empty blade crews accept any job
                                     any(crew in blade_crews for crew in job_crews))
                        
                        print(f"  {blade['name']} (nimby: {blade.get('nimby', 'unknown')}):")
                        print(f"    Services: {blade_services} (matches: {service_match})")
                        print(f"    Envkeys: {blade_envkeys} (matches: {envkey_match})")
                        print(f"    Crews: {blade_crews} (matches: {crews_match})")
                        
                        if service_match and envkey_match and crews_match and blade.get('nimby', 'off') == 'off':
                            compatible_blades.append(blade['name'])
                    
                    if compatible_blades:
                        print(f"[DEBUG] ✅ Job should be picked up by: {compatible_blades}")
                    else:
                        print(f"[DEBUG] ❌ No compatible blades found!")
                        print(f"[DEBUG] Job requires: service={job_service}, envkey={job_envkey}, crews={job_crews}")
                        active_blades = [b['name'] for b in blade_info if b.get('nimby', 'off') == 'off']
                        print(f"[DEBUG] Active blades: {active_blades}")
                        
                else:
                    print("[DEBUG] No blade information available for comparison")
                
            except Exception as e:
                err_msg = f"Error on {write_name}: {type(e).__name__}: {e}"
                print("[TractorSpool] " + err_msg)
    
                log_path = os.path.join(os.path.dirname(__file__), "tractor_spool_log.json")
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, "a") as log:
                    log.write(err_msg + "\n")
    
                QtWidgets.QMessageBox.critical(self, "Submission Failed", err_msg)
                errors += 1

        # Restore original Write node paths
        restored_count = 0
        for write_name, original_path in original_write_paths.items():
            try:
                write_node = nuke.toNode(write_name)
                if write_node and 'file' in write_node.knobs():
                    current_path = write_node['file'].value()
                    if current_path != original_path:
                        write_node['file'].setValue(original_path)
                        restored_count += 1
                        print(f"[DEBUG] Restored Write node '{write_name}' path: {original_path}")
            except Exception as restore_e:
                print(f"[WARNING] Could not restore Write node '{write_name}' path: {restore_e}")
        
        if restored_count > 0:
            print(f"[DEBUG] Restored {restored_count} Write node paths to original values")
            # Save the script to preserve the original paths
            try:
                nuke.scriptSave()
                print(f"[DEBUG] Saved script with restored Write node paths")
            except Exception as save_e:
                print(f"[WARNING] Could not save script after restoring paths: {save_e}")

        if errors == 0:
            self.showJobSubmissionSuccess(submitted_jobs)

    def showJobSubmissionSuccess(self, submitted_jobs):
        """Show custom success dialog with clickable links to submitted jobs"""
        if not submitted_jobs:
            QtWidgets.QMessageBox.information(self, "Submitted", "Jobs submitted to Tractor.")
            return
        
        # Create custom dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Jobs Submitted Successfully")
        dialog.setMinimumSize(500, 300)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Success message
        success_label = QtWidgets.QLabel(f"✅ Successfully submitted {len(submitted_jobs)} job(s) to Tractor!")
        success_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2E7D32; margin-bottom: 15px;")
        layout.addWidget(success_label)
        
        # Job list with clickable links
        scroll_area = QtWidgets.QScrollArea()
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        
        for job_info in submitted_jobs:
            job_id = job_info['id']
            job_title = job_info['title']
            write_node = job_info['write_node']
            
            # Job info container
            job_container = QtWidgets.QFrame()
            job_container.setStyleSheet("""
                QFrame {
                    border: 1px solid #E0E0E0;
                    border-radius: 5px;
                    padding: 8px;
                    margin: 2px;
                    background-color: #F8F9FA;
                }
            """)
            job_layout = QtWidgets.QVBoxLayout(job_container)
            
            # Job title and write node
            job_info_label = QtWidgets.QLabel(f"<b>Write Node:</b> {write_node}")
            job_info_label.setStyleSheet("font-size: 12px; margin-bottom: 3px;")
            job_layout.addWidget(job_info_label)
            
            # Job ID with clickable link
            # Tractor web interface typically uses URL format: http://server/tv/#jid=JOB_ID
            tractor_url = f"http://10.31.240.8/tv/#jid={job_id}"
            job_link = QtWidgets.QLabel(f'<a href="{tractor_url}" style="color: #1976D2; text-decoration: none;">🎬 View Job {job_id} in Tractor</a>')
            job_link.setOpenExternalLinks(True)
            job_link.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    padding: 4px;
                }
                QLabel:hover {
                    background-color: #E3F2FD;
                    border-radius: 3px;
                }
            """)
            job_link.setToolTip(f"Click to open Job {job_id} in Tractor web interface")
            job_layout.addWidget(job_link)
            
            scroll_layout.addWidget(job_container)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # General Tractor link
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(separator)
        
        general_link = QtWidgets.QLabel('<a href="http://10.31.240.8/tv/" style="color: #4A90E2; text-decoration: none;">🔗 Open Tractor Monitor (All Jobs)</a>')
        general_link.setOpenExternalLinks(True)
        general_link.setStyleSheet("font-size: 12px; text-align: center; margin: 10px;")
        general_link.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(general_link)
        
        # Close button
        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        close_button.clicked.connect(dialog.accept)
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        dialog.exec_()

class TractorSpoolUIHelp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TractorSpoolUIHelp, self).__init__(parent)
        self.setWindowTitle("TractorSpool - Help")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Make dialog resizable and set modal behavior
        self.setModal(False)  # Allow interaction with main window
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Clean up when closed
        
        self.setupUI()
        self.loadHelpContent()
    
    def closeEvent(self, event):
        print("[Help UI] Closed")
        super().closeEvent(event)

    def __del__(self):
        print("[Help UI] Python __del__ called")

    def setupUI(self):
        """Setup the help window UI"""
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Title/Header
        header_label = QtWidgets.QLabel(tractorSpoolHelpWindowTitle)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_font = header_label.font()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        main_layout.addWidget(header_label)
        
        # Help content area - using QTextEdit for rich text and scrolling
        self.help_text_edit = QtWidgets.QTextEdit()
        self.help_text_edit.setReadOnly(True)
        self.help_text_edit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        
        # Style the text area
        self.help_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                border: 1px solid #cccccc;
                padding: 10px;
                font-family: Arial, sans-serif;
                font-size: 11pt;
            }
        """)
        
        main_layout.addWidget(self.help_text_edit)
        
        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        # Close button
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setMinimumWidth(100)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)

    def loadHelpContent(self):
        """Load and display the help content - customize this method with your text"""
        help_content = self.getHelpText()
        self.help_text_edit.setHtml(help_content)

    def getHelpText(self):
        """Return the help content as HTML"""
        return f"""
        <h2>TractorSpool User Guide</h2>
        <hr>

        <h3>Overview</h3>
        <p>TractorSpool is a NUKE tool designed to help you launching NUKE jobs to your local Tractor Dispatcher. </p>
        <p>It provides a three-column browser interface to quickly fetch all [Read] nodes of the scene & spool them to Tractor.</p>
        
        <h3>Interface Layout</h3>
        <ul>
            <li><strong>Column 1 - Write Nodes:</strong> Lists all existing [Read] nodes in your current script.</li>
            <li><strong>Column 2 - Spool Settings:</strong> Lists all SpoolSettings before dispatching your job.</li>
            <li><strong>Column 3 - Tractor Monitor:</strong> Direct link to Tractor web interface for job monitoring</li>
        </ul>
        
        <h3>How to Use</h3>
        <ol>
            <li><strong>Select [Read](s):</strong> Click on one or multiple [Read] nodes in the first column</li>
            <li><strong>Adjust SpoolSettings:</strong> Tweak your SpoolSettings in the second column</li>
            <li><strong>Spool Job:</strong> Click on 'SPOOL JOB' to get your job dispatched on Tractor</li>
            <li><strong>Tractor Refresh:</strong> Click on 'Refresh Job List' to double-check that your job is on Tractor</li>
            <li><strong>Job Overview:</strong> Check on your job's progres via TractorSpool or direcly on Tractor.</li>
        </ol>
        
        <h3>Features</h3>
        <ul>
            <li><strong>Dynamic [Write] nodes list:</strong> [Write] nodes from the opened script are all listed & this list can be refreshed</li>
            <li><strong>Exposed Spool Settings:</strong> Spool Settings can all be edited in TractorSpool, including Priority & Project</li>
            <li><strong>Path Flexibility:</strong> Supports both local drives and UNC network paths</li>
            <li><strong>Tractor Jobs Connectivity:</strong> Displays jobs dispatched on Tractor with sufficient details</li>
        </ul>
        
        <h3>Configuration</h3>
        <p><strong>Active Projects:</strong> Create a 'live_projects.json' file in your ~/.nuke/tractor/ directory 
        to specify which projects should be displayed in the 'Project' list.</p>
        
        <h3>Tips</h3>
        <ul>
            <li>All [Read] nodes are shown with their names, so name them depending on their purposes (e.g. 'Write_COMP', 'Write_PRECOMP')</li>
            <li>You can keep the TractorSpool window open while working in NUKE</li>
        </ul>
        
        <h3>Troubleshooting</h3>
        <p><strong> -- Needs to be documented once this tool gets under production pressure.</p>
        
        <hr>
        <p><em>For additional support or feature requests, contact Loucas RONGEART -- <a href="mailto:{contactLR}">{contactLR}</a></em></p>
        <p><em>TractorSpool {tractorSpoolVersion}</p>
        """

    def setHelpContent(self, content):
        """Set custom help content (can be plain text or HTML)"""
        if isinstance(content, str):
            if content.strip().startswith('<'):
                # Assume HTML content
                self.help_text_edit.setHtml(content)
            else:
                # Plain text content
                self.help_text_edit.setPlainText(content)
        else:
            self.help_text_edit.setPlainText(str(content))

    def appendHelpContent(self, content):
        """Append additional content to existing help text"""
        current_content = self.help_text_edit.toHtml()
        if isinstance(content, str):
            if content.strip().startswith('<'):
                # HTML content
                new_content = current_content + content
                self.help_text_edit.setHtml(new_content)
            else:
                # Plain text - convert to HTML and append
                self.help_text_edit.moveCursor(QtWidgets.QTextCursor.End)
                self.help_text_edit.insertPlainText(content)




def launch_submit_to_tractor_ui():
    global submit_ui_instance

    if submit_ui_instance and submit_ui_instance.isVisible():
        submit_ui_instance.close()
        submit_ui_instance = None

    submit_ui_instance = SubmitToTractorUI()
    submit_ui_instance.show()


def launch_help_window():
    global help_ui_instance

    try:
        if help_ui_instance and isValid(help_ui_instance) and help_ui_instance.isVisible():
            help_ui_instance.close()
            help_ui_instance = None
    except Exception as e:
        print(f"[TractorSpoolManager] Safe cleanup error: {e}")
        help_ui_instance = None

    help_ui_instance = TractorSpoolUIHelp()
    help_ui_instance.show()