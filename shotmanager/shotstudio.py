# ShotStudio.py

import nuke
import getpass
import os
import json
import re
from PySide2 import QtWidgets, QtCore, QtGui


PROJECTS_ROOT = "E:/SHOWS"
JSON_PATH = os.path.join(os.path.dirname(__file__), "live_projects.json")


username = getpass.getuser()
shotstudioVersion = "v1.1"
shotstudioWindowTitle = 'ShotStudio {}'.format(shotstudioVersion)
shotstudioHelpWindowTitle = 'ShotManager Help {}'.format(shotstudioVersion)


class SequenceListItemWidget(QtWidgets.QWidget):
    def __init__(self, seq_name):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(6)

        # Load .png icon instead of colored box
        icon_path = os.path.join(os.path.dirname(__file__), "icon", "script", "folder.png")
        if os.path.exists(icon_path):
            icon_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(icon_path)
            pixmap = pixmap.scaled(12, 12, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            layout.addWidget(icon_label)
        else:
            print(f"[WARN] Icon not found at {icon_path}")

        # Label
        self.label = QtWidgets.QLabel(seq_name)
        self.label.setObjectName("seqLabel")
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        layout.addStretch()
        self.setLayout(layout)



class ShotListItemWidget(QtWidgets.QWidget):
    def __init__(self, shot_name, has_comp=False, has_slap=False, has_previz=False):
        super().__init__()
        self.shot_name = shot_name

        # Layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(6)

        # Dot icons
        dot_layout = QtWidgets.QHBoxLayout()
        dot_layout.setContentsMargins(0, 0, 0, 0)
        dot_layout.setSpacing(4)
        if has_previz:
            dot_layout.addWidget(self._make_dot("#ff3333", "PreViz"))
        if has_slap:
            dot_layout.addWidget(self._make_dot("#00ff22", "SlapComp"))
        if has_comp:
            dot_layout.addWidget(self._make_dot("#002fff", "Comp"))

        dot_container = QtWidgets.QWidget()
        dot_container.setLayout(dot_layout)
        dot_container.setFixedWidth(36)

        # Shot name label
        self.label = QtWidgets.QLabel(shot_name)
        self.label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.label.setStyleSheet("color: white; background-color: transparent; padding: 0px 4px;")
        self.label.setMinimumHeight(18)

        layout.addWidget(dot_container)
        layout.addWidget(self.label)
        layout.addStretch()
        self.setFixedHeight(24)

    def _make_dot(self, color, tooltip):
        dot = QtWidgets.QLabel()
        dot.setFixedSize(8, 8)
        dot.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
        dot.setToolTip(tooltip)
        return dot

    def set_selected(self, is_selected):
        """Update style to reflect selection."""
        if is_selected:
            self.label.setStyleSheet("color: white; background-color: rgba(255, 120, 0, 80); padding: 0px 4px;")
        else:
            self.label.setStyleSheet("color: white; background-color: transparent; padding: 0px 4px;")





class ShotStudio(QtWidgets.QWidget):
    def __init__(self):
        super(ShotStudio, self).__init__()

        self.setWindowTitle("ShotManager - Studio")
        self.resize(800, 200)
        self.permission_denied = False
        self.username = getpass.getuser()

        # Check active users
        users_file = os.path.join(os.path.dirname(__file__), "active_users.json")
        allowed_users = []
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r') as f:
                    allowed_users = json.load(f)
            except Exception as e:
                print(f"[ShotStudio] Failed to read active_users.json: {e}")

        if self.username not in allowed_users:
            self.permission_denied = True
            self.setupPermissionDeniedUI()
            return

        self.default_button_style = """
            QPushButton {
                background-color: #2a2a2a;
                color: #888888;
                border: 1px solid #444;
                padding: 6px 12px;
            }
        """
        self.manual_version_selected = False
        


        self.setupUI()
        self.load_shows()

        # Signal connections
        self.showCombo.currentTextChanged.connect(self.load_sequences_for_show)
        self.seqList.itemSelectionChanged.connect(self.on_sequence_selected)
    

    def on_sequence_selected(self):
        current_item = self.seqList.currentItem()
        if not current_item:
            return

        seq_widget = self.seqList.itemWidget(current_item)
        seq_name = seq_widget.label.text() if seq_widget else ""
        if seq_name:
            self.load_shots_for_sequence(seq_name)


    def setupUI(self):
        # --- Widgets ---
        self.showCombo = QtWidgets.QComboBox()
        self.seqList = QtWidgets.QListWidget()
        self.shotList = QtWidgets.QListWidget()
        self.shotList.setStyleSheet("""
            QListWidget {
                background-color: #111;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #333333;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #222;
            }
        """)

        self.seqList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.shotList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.shotList.itemSelectionChanged.connect(self.on_shot_selected)

        # --- Header Layout ---
        header_layout = QtWidgets.QHBoxLayout()
        icon_path = os.path.join(os.path.dirname(__file__), "icon/shotStudio.png")
        if os.path.exists(icon_path):
            icon_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(icon_path)
            pixmap = pixmap.scaledToHeight(48, QtCore.Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            header_layout.addWidget(icon_label)

        header_label = QtWidgets.QLabel(shotstudioWindowTitle)
        header_font = header_label.font()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_layout.addWidget(header_label)
        header_layout.addStretch()

        user_label = QtWidgets.QLabel(f"Logged in as: {getpass.getuser()}")
        user_label.setAlignment(QtCore.Qt.AlignRight)

        # --- Show Selector ---
        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addStretch()
        topLayout.addWidget(QtWidgets.QLabel("Select Show:"))
        topLayout.addWidget(self.showCombo)

        # --- Divider Line ---
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)

        # --- Preview Label ---
        self.previewLabel = QtWidgets.QLabel("No Preview")
        self.previewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.previewLabel.setScaledContents(True)
        self.previewLabel.setFixedSize(950, 540)
        self.previewLabel.setStyleSheet("background-color: #1a1a1a; border: 1px solid #444; color: #ddd;")

        # --- Filename label below preview ---
        self.previewFilenameLabel = QtWidgets.QLabel("")
        self.previewFilenameLabel.setFixedWidth(950)  # Match preview image width
        self.previewFilenameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.previewFilenameLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # Optional: make text selectable
        self.previewFilenameLabel.setStyleSheet("""
            color: rgba(255, 255, 255, 150);
            background-color: rgba(0, 0, 0, 120);
            padding: 2px 6px;
            font-size: 10px;
            border-radius: 4px;
        """)
        # Make it visible by default, even if it's empty
        self.previewFilenameLabel.setText("No preview loaded")
        self.previewFilenameLabel.setMinimumHeight(20)
        self.previewFilenameLabel.show()

        # --- Slider Layout ---
        sliderLayout = QtWidgets.QHBoxLayout()
        self.sliderLeftLabel = QtWidgets.QLabel("0")
        self.sliderRightLabel = QtWidgets.QLabel("0")
        self.sliderLeftLabel.setStyleSheet("color: white;")
        self.sliderRightLabel.setStyleSheet("color: white;")
        self.previewSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.previewSlider.setMinimum(0)
        self.previewSlider.setSingleStep(1)
        self.previewSlider.setEnabled(False)
        self.previewSlider.valueChanged.connect(self.update_preview_frame)
        sliderLayout.addWidget(self.sliderLeftLabel)
        sliderLayout.addWidget(self.previewSlider)
        sliderLayout.addWidget(self.sliderRightLabel)

        # --- Preview Layout ---
        previewLayout = QtWidgets.QVBoxLayout()
        previewTitle = QtWidgets.QLabel("<b>PREVIEW</b>")
        previewLayout.addWidget(previewTitle)
        previewLayout.addWidget(self.previewLabel)

        # Add filename label in its own row
        filenameRow = QtWidgets.QHBoxLayout()
        filenameRow.addStretch()
        filenameRow.addWidget(self.previewFilenameLabel)
        previewLayout.addSpacing(4)
        previewLayout.addLayout(filenameRow)

        # Add slider under filename
        previewLayout.addLayout(sliderLayout)

        # --- Sequence Column ---
        seqWidget = QtWidgets.QWidget()
        seqLayout = QtWidgets.QVBoxLayout(seqWidget)
        seqLayout.setContentsMargins(0, 0, 0, 0)
        seqTitle = QtWidgets.QLabel("<b>SEQUENCES</b>")
        seqLayout.addWidget(seqTitle)
        seqLayout.addWidget(self.seqList)
        seqWidget.setStyleSheet("""
            background-color: #222;
            color: white;
            border: 1px solid gray;
        """)

        # --- Shot Column ---
        shotWidget = QtWidgets.QWidget()
        shotLayout = QtWidgets.QVBoxLayout(shotWidget)
        shotLayout.setContentsMargins(0, 0, 0, 0)
        shotTitle = QtWidgets.QLabel("<b>SHOTS</b>")
        shotLayout.addWidget(shotTitle)
        shotLayout.addWidget(self.shotList)
        shotWidget.setStyleSheet("""
            background-color: #222;
            color: white;
            border: 1px solid gray;
        """)

        legendLayout = QtWidgets.QHBoxLayout()
        legendLayout.setSpacing(10)

        def legend_item(color, label):
            swatch = QtWidgets.QLabel()
            swatch.setFixedSize(10, 10)
            swatch.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
            text = QtWidgets.QLabel(label)
            text.setStyleSheet("color: white;")
            container = QtWidgets.QHBoxLayout()
            container.addWidget(swatch)
            container.addWidget(text)
            container.setContentsMargins(0, 0, 0, 0)
            widget = QtWidgets.QWidget()
            widget.setLayout(container)
            return widget

        legendLayout.addWidget(legend_item("#ff3333", "PreViz"))
        legendLayout.addWidget(legend_item("#00ff22", "SlapComp"))
        legendLayout.addWidget(legend_item("#002fff", "Comp"))
        legendLayout.addStretch()
        shotLayout.addLayout(legendLayout)

        # --- Info Panel ---
        infoLayout = QtWidgets.QVBoxLayout()
        infoTitle = QtWidgets.QLabel("<b>SHOT INFOS</b>")
        infoLayout.addWidget(infoTitle)

        self.frameRangeLabel = QtWidgets.QLabel("Frame Range: N/A")
        infoLayout.addWidget(self.frameRangeLabel)

        infoLayout.addWidget(QtWidgets.QLabel("<b>Version Folder:</b>"))
        versionRow = QtWidgets.QHBoxLayout()
        self.versionCombo = QtWidgets.QComboBox()
        self.versionCombo.currentTextChanged.connect(self.on_version_changed)
        infoLayout.addWidget(self.versionCombo)

        self.latestTagLabel = QtWidgets.QLabel()
        self.latestTagLabel.setStyleSheet("color: orange; font-weight: bold;")
        versionRow.addWidget(self.latestTagLabel)

        self.previewTypeCombo = QtWidgets.QComboBox()
        self.previewTypeCombo.addItems(["Comp", "SlapComp", "PreViz"])
        self.previewTypeCombo.setCurrentText("Comp")
        self.previewTypeCombo.currentTextChanged.connect(self.on_preview_type_changed)
        infoLayout.addWidget(QtWidgets.QLabel("Preview Type:"))
        infoLayout.addWidget(self.previewTypeCombo)
        infoLayout.addLayout(versionRow)

        self.loadMovButton = QtWidgets.QPushButton("Load .mov")
        self.loadMovButton.clicked.connect(self.on_load_mov_clicked)
        self.writeMovButton = QtWidgets.QPushButton("Write .mov")
        self.writeMovButton.clicked.connect(self.on_write_mov_clicked)
        self.loadNkButton = QtWidgets.QPushButton("Load .nk")
        self.loadNkButton.clicked.connect(self.on_load_nk_clicked)
        infoLayout.addWidget(self.loadMovButton)
        infoLayout.addWidget(self.writeMovButton)
        infoLayout.addWidget(self.loadNkButton)
        infoLayout.addStretch()

        # --- Browser Layout ---
        browserLayout = QtWidgets.QHBoxLayout()
        browserLayout.addWidget(seqWidget, 1)
        browserLayout.addWidget(shotWidget, 1)
        browserLayout.addLayout(infoLayout, 1)
        browserLayout.addLayout(previewLayout, 0)

        # --- Main Layout ---
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(header_layout)
        mainLayout.addWidget(user_label)
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(divider)
        mainLayout.addLayout(browserLayout)

        self.setLayout(mainLayout)

    def setupPermissionDeniedUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("<b>You do not have user permission to use that tool.<br> Application features are restricted for '{}'</b>".format(getpass.getuser()))
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)

        self.setLayout(layout)
        self.permission_denied = True



    def refresh_preview(self, shot_path):
        self.preview_images = self.get_preview_images(shot_path)

        if self.preview_images:
            self.previewSlider.setMaximum(len(self.preview_images) - 1)
            self.previewSlider.setValue(0)
            self.previewSlider.setEnabled(True)
            self.previewSlider.show()
            self.sliderLeftLabel.show()
            self.sliderRightLabel.show()
            self.sliderRightLabel.setText(str(len(self.preview_images) - 1))
            self.sliderLeftLabel.setText("0")
            self.update_preview_frame(0)
        else:
            self.previewLabel.setPixmap(QtGui.QPixmap())
            self.previewLabel.setText("No Preview Found")
            self.previewSlider.hide()
            self.sliderLeftLabel.hide()
            self.sliderRightLabel.hide()
            self.previewFilenameLabel.setText("No preview found")


    def load_shows(self):
        if not os.path.exists(JSON_PATH):
            QtWidgets.QMessageBox.critical(self, "Error", f"{JSON_PATH} not found.")
            return

        with open(JSON_PATH, "r") as f:
            data = json.load(f)

        active_shows = [k for k, v in data.items() if v.get("status") == "active"]
        self.showCombo.addItems(sorted(active_shows))


    def load_sequences_for_show(self, show_name):
        self.seqList.clear()
        self.shotList.clear()
        self.previewLabel.clear()

        show_root = os.path.join(PROJECTS_ROOT, show_name)
        self.current_show_path = find_case_insensitive_folder(show_root, "shots")

        if not self.current_show_path:
            print(f"[WARN] Could not find a 'shots' folder in: {show_root}")
            return

        sequences = [
            d for d in os.listdir(self.current_show_path)
            if os.path.isdir(os.path.join(self.current_show_path, d))
        ]

        for seq in sorted(sequences):
            item_widget = SequenceListItemWidget(seq)
            item = QtWidgets.QListWidgetItem(self.seqList)
            item.setSizeHint(item_widget.sizeHint())
            self.seqList.addItem(item)
            self.seqList.setItemWidget(item, item_widget)

        # Auto-select first sequence
        if self.seqList.count() > 0:
            self.seqList.setCurrentRow(0)
            QtCore.QTimer.singleShot(0, lambda: self.seqList.itemSelectionChanged.emit())



    def load_shots_for_sequence(self, seq_name):
        self.shotList.clear()
        seq_path = os.path.join(self.current_show_path, seq_name)
        if not os.path.exists(seq_path):
            return

        shots = [
            d for d in os.listdir(seq_path)
            if os.path.isdir(os.path.join(seq_path, d))
        ]

        for shot in sorted(shots):
            shot_path = os.path.join(seq_path, shot)
            print(f"[DEBUG] Inspecting shot folder: {shot_path}")

            nuke_path = find_folder_recursive(shot_path, "nuke")
            out_path = find_folder_recursive(nuke_path, "OUT") if nuke_path else None
            has_comp = has_slap = has_previz = False
            if out_path:
                has_comp = find_case_insensitive_folder(out_path, "Comp") is not None
                has_slap = find_case_insensitive_folder(out_path, "SlapComp") is not None
                has_previz = find_case_insensitive_folder(out_path, "PreViz") is not None

            # Add visual indicator to the shot list (even if no comp/slap/previz)
            item_widget = ShotListItemWidget(shot, has_comp, has_slap, has_previz)
            item = QtWidgets.QListWidgetItem(self.shotList)
            item.setSizeHint(QtCore.QSize(0, 24))
            self.shotList.addItem(item)
            self.shotList.setItemWidget(item, item_widget)

        # Auto-select the first shot after shots are populated
        if self.shotList.count() > 0:
            self.shotList.setCurrentRow(0)
            QtCore.QTimer.singleShot(0, self.on_shot_selected)




    def on_preview_type_changed(self, new_type):
        print(f"[INFO] Preview type changed to: {new_type}")
        self.manual_version_selected = False  # Reset override so latest is picked
        self.on_shot_selected()



    def get_preview_images(self, shot_path):
        def safe_find(parent, child):
            if not parent:
                return None
            return find_case_insensitive_folder(parent, child)

        nuke_path = safe_find(shot_path, "nuke")
        out_path = safe_find(nuke_path, "OUT")
        phase = self.previewTypeCombo.currentText()
        phase_path = safe_find(out_path, phase)

        version = self.versionCombo.currentData()
        if not (phase_path and version):
            print(f"[WARN] Missing version or phase path: phase_path={phase_path}, version={version}")
            return []

        version_path = os.path.join(phase_path, version)
        if not os.path.isdir(version_path):
            print(f"[WARN] Version path does not exist: {version_path}")
            return []

        jpg_path = safe_find(version_path, "jpg")
        if not jpg_path:
            print(f"[WARN] Could not find 'jpg' folder inside {version_path}")
            return []

        images = sorted([
            os.path.join(jpg_path, f)
            for f in os.listdir(jpg_path)
            if f.lower().endswith((".jpg", ".jpeg"))
        ])
        return images





    def on_preview_type_changed(self, new_type):
        self.on_shot_selected()  # Just trigger a refresh of the selected shot


    def on_load_mov_clicked(self):
        selected_items = self.shotList.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "No Shot Selected", "Please select a shot first.")
            return

        shot_name = selected_items[0].text()
        current_item = self.seqList.currentItem()
        seq_widget = self.seqList.itemWidget(current_item)
        seq_name = seq_widget.label.text() if seq_widget else ""
        shot_path = os.path.join(self.current_show_path, seq_name, shot_name)

        # Navigate to MOV folder
        phase = self.previewTypeCombo.currentText()
        mov_dir = os.path.join(shot_path, "nuke", "OUT", phase, "mov")

        if not os.path.isdir(mov_dir):
            QtWidgets.QMessageBox.warning(self, "Missing .mov Folder", f"No folder found: {mov_dir}")
            return

        movs = [f for f in os.listdir(mov_dir) if f.lower().endswith(".mov")]
        if not movs:
            QtWidgets.QMessageBox.information(self, "No .mov Found", f"No .mov files in {mov_dir}")
            return

        mov_path = os.path.join(mov_dir, movs[0])
        print(f"[DEBUG] Opening MOV: {mov_path}")

        try:
            os.startfile(mov_path)  # Windows-specific
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not open .mov:\n{e}")

    
    def on_write_mov_clicked(self):
        import nuke

        if not nuke.root().name():
            QtWidgets.QMessageBox.warning(self, "No Script Opened", "Please open a .nk script before writing a .mov.")
            return

        selected_items = self.shotList.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "No Shot Selected", "Please select a shot first.")
            return

        shot_name = selected_items[0].text()
        current_item = self.seqList.currentItem()
        seq_widget = self.seqList.itemWidget(current_item)
        seq_name = seq_widget.label.text() if seq_widget else ""
        shot_path = os.path.join(self.current_show_path, seq_name, shot_name)
        phase = self.previewTypeCombo.currentText()

        mov_dir = os.path.join(shot_path, "nuke", "OUT", phase, "mov")
        os.makedirs(mov_dir, exist_ok=True)

        mov_path = os.path.join(mov_dir, f"{shot_name}_{phase}.mov").replace("\\", "/")

        # Get frame range
        start = int(nuke.root().firstFrame())
        end = int(nuke.root().lastFrame())

        # Create Write node
        write_node = nuke.createNode("Write", inpanel=False)
        write_node["file_type"].setValue("mov")
        write_node["file"].setValue(mov_path)
        write_node["meta_codec"].setValue("h264")
        write_node["mov64_fps"].setValue(int(nuke.root()["fps"].value()))

        try:
            nuke.execute(write_node, start, end)
            QtWidgets.QMessageBox.information(self, "Done", f".mov written to:\n{mov_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not write .mov:\n{e}")
        finally:
            nuke.delete(write_node)


    def on_load_nk_clicked(self):
        import nuke

        selected_items = self.shotList.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "No Shot Selected", "Please select a shot first.")
            return

        shot_name = selected_items[0].text()
        current_item = self.seqList.currentItem()
        seq_widget = self.seqList.itemWidget(current_item)
        seq_name = seq_widget.label.text() if seq_widget else ""
        shot_path = os.path.join(self.current_show_path, seq_name, shot_name)
        phase = self.previewTypeCombo.currentText()

        nk_dir = os.path.join(shot_path, "nuke", "OUT", phase, "nk")
        if not os.path.isdir(nk_dir):
            QtWidgets.QMessageBox.warning(self, "Missing .nk Folder", f"No folder found: {nk_dir}")
            return

        nk_files = [f for f in os.listdir(nk_dir) if f.lower().endswith(".nk")]
        if not nk_files:
            QtWidgets.QMessageBox.information(self, "No .nk Found", f"No .nk files in {nk_dir}")
            return

        if len(nk_files) == 1:
            selected_nk = nk_files[0]
        else:
            selected_nk, ok = QtWidgets.QInputDialog.getItem(
                self, "Select Nuke Script", "Multiple .nk files found:", nk_files, 0, False
            )
            if not ok:
                return

        nk_path = os.path.join(nk_dir, selected_nk).replace("\\", "/")
        print(f"[DEBUG] Loading NK script: {nk_path}")

        try:
            nuke.scriptOpen(nk_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not open .nk:\n{e}")

    

    def on_shot_selected(self):
        selected_items = self.shotList.selectedItems()

        # Highlight selected shot item
        for i in range(self.shotList.count()):
            item = self.shotList.item(i)
            widget = self.shotList.itemWidget(item)
            if widget:
                is_selected = item in self.shotList.selectedItems()
                widget.set_selected(is_selected)


        if not selected_items:
            # Reset selection
            self.previewLabel.setText("No Preview")
            self.previewLabel.setPixmap(QtGui.QPixmap())
            self.frameRangeLabel.setText("Frame Range: N/A")
            self.versionCombo.clear()
            self.versionCombo.setEnabled(False)
            self.latestTagLabel.setText("")
            self.manual_version_selected = False  # Reset here when selection is cleared
            return

        # --- Begin Shot Change ---
        # Reset manual selection when shot changes
        self.manual_version_selected = False

        # --- Resolve shot and sequence paths ---
        item = selected_items[0]
        widget = self.shotList.itemWidget(item)
        shot_name = widget.label.text()
        current_item = self.seqList.currentItem()
        seq_widget = self.seqList.itemWidget(current_item)
        seq_name = seq_widget.label.text() if seq_widget else ""
        shot_path = os.path.join(self.current_show_path, seq_name, shot_name)

        # --- Load Frame Range ---
        json_path = os.path.join(shot_path, "shotinfo.json")
        if os.path.isfile(json_path):
            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
                start = data.get("startFrame", "N/A")
                end = data.get("endFrame", "N/A")
                self.frameRangeLabel.setText(f"Frame Range: {start} - {end}")
            except Exception as e:
                print(f"[ERROR] Failed to read {json_path}: {e}")
                self.frameRangeLabel.setText("Frame Range: Error")
        else:
            self.frameRangeLabel.setText("Frame Range: N/A")

        # --- Setup versionCombo ---
        self.versionCombo.blockSignals(True)
        self.versionCombo.clear()
        self.latestTagLabel.setText("")

        phase = self.previewTypeCombo.currentText()
        nuke_path = find_case_insensitive_folder(shot_path, "nuke")
        out_path = find_case_insensitive_folder(nuke_path, "OUT") if nuke_path else None
        phase_path = find_case_insensitive_folder(out_path, phase) if out_path else None

        selected_version = None
        latest_version = None

        if not phase_path:
            self.versionCombo.setEnabled(False)
            self.versionCombo.addItem("[No Versions]")
            self.versionCombo.blockSignals(False)
            self.manual_version_selected = False  # Reset override when nothing to select
            return

        try:
            versions = sorted([
                d for d in os.listdir(phase_path)
                if os.path.isdir(os.path.join(phase_path, d)) and d.lower().startswith("v")
            ])
            if not versions:
                self.versionCombo.setEnabled(False)
                self.versionCombo.addItem("[Empty]")
                self.versionCombo.blockSignals(False)
                self.manual_version_selected = False
                return

            latest_version = versions[-1]
            self.versionCombo.setEnabled(True)

            for v in versions:
                label = f"{v} (Latest)" if v == latest_version else v
                self.versionCombo.addItem(label, userData=v)

            if self.manual_version_selected:
                selected_version = self.versionCombo.currentData()
                if selected_version not in versions:
                    print(f"[INFO] Manual version {selected_version} not valid. Falling back to latest.")
                    selected_version = latest_version
                    self.manual_version_selected = False
            else:
                selected_version = latest_version

            for i in range(self.versionCombo.count()):
                if self.versionCombo.itemData(i) == selected_version:
                    self.versionCombo.setCurrentIndex(i)
                    self.latestTagLabel.setText("Latest" if selected_version == latest_version else "")
                    break

        except Exception as e:
            print(f"[ERROR] Could not read versions: {e}")
            self.versionCombo.setEnabled(False)
            self.versionCombo.addItem("[Error]")
            self.manual_version_selected = False

        self.versionCombo.blockSignals(False)

        # --- Defer refresh until versionCombo is finalized ---
        QtCore.QTimer.singleShot(0, lambda: self.refresh_preview(shot_path))



    def update_preview_frame(self, index):
        if hasattr(self, 'preview_images') and 0 <= index < len(self.preview_images):
            image_path = self.preview_images[index]
            pixmap = QtGui.QPixmap(image_path)
            self.previewLabel.setPixmap(pixmap)

            self.sliderLeftLabel.setText(str(index))
            self.sliderRightLabel.setText(str(len(self.preview_images) - 1))

            # Extract and format the filename with color
            filename = os.path.basename(image_path)

            # Example: sh010_v003.0123.jpg → extract shot, version, and frame
            import re
            match = re.match(r"(.*?)(_v\d+)?\.(\d+)\.(jpg|jpeg)", filename, re.IGNORECASE)
            if match:
                shot = match.group(1)
                version = match.group(2) or ""
                frame = match.group(3)

                colored_text = (
                    f"<span style='color:#ff4444;'>{shot}</span>"
                    f"<span style='color:#00ffff;'>{version}</span>."
                    f"<span style='color:#ffff00;'>{frame}</span>.jpg"
                )
                self.previewFilenameLabel.setText(colored_text)
            else:
                self.previewFilenameLabel.setText(filename)

            self.previewFilenameLabel.show()
        else:
            self.previewFilenameLabel.setText







    def on_version_changed(self, new_version):
        print(f"[INFO] Version manually changed to: {new_version}")
        self.manual_version_selected = True  # <-- mark manual override

        selected_items = self.shotList.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        widget = self.shotList.itemWidget(item)
        shot_name = widget.label.text()
        current_item = self.seqList.currentItem()
        seq_widget = self.seqList.itemWidget(current_item)
        seq_name = seq_widget.label.text() if seq_widget else ""
        shot_path = os.path.join(self.current_show_path, seq_name, shot_name)

        self.refresh_preview(shot_path)

        selected_version = self.versionCombo.currentData()
        latest_version = self.versionCombo.itemData(self.versionCombo.count() - 1)
        self.latestTagLabel.setText("Latest" if selected_version == latest_version else "")







def find_case_insensitive_folder(parent_path, target_name):
    """Returns the full path to a folder containing target_name (case-insensitive, affixes allowed), or None."""
    try:
        pattern = re.compile(re.escape(target_name), re.IGNORECASE)
        for name in os.listdir(parent_path):
            full_path = os.path.join(parent_path, name)
            if pattern.search(name) and os.path.isdir(full_path):
                return full_path
    except FileNotFoundError:
        pass
    return None


def find_folder_recursive(parent_path, target_name):
    """Recursively search for a folder containing target_name (case-insensitive, affixes allowed) and return its path, or None."""
    import re
    pattern = re.compile(re.escape(target_name), re.IGNORECASE)
    for root, dirs, files in os.walk(parent_path):
        for d in dirs:
            if pattern.search(d):
                return os.path.join(root, d)
    return None




# To run inside Nuke:
def launch_shotstudio():
    global shotstudio_widget
    try:
        shotstudio_widget.close()
        shotstudio_widget.deleteLater()
    except:
        pass
    shotstudio_widget = ShotStudio()
    shotstudio_widget.show()
