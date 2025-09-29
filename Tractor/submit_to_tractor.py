import nuke
import tractor.api.query as tq
import os



def submit_to_tractor():
    script_path = nuke.root().name()
    if script_path == "Root":
        nuke.message("Please save your script before submitting to Tractor.")
        return

    first_frame = int(nuke.root()['first_frame'].value())
    last_frame = int(nuke.root()['last_frame'].value())
    write_nodes = [n for n in nuke.allNodes('Write') if not n['disable'].value()]

    if not write_nodes:
        nuke.message("No enabled Write nodes found.")
        return

    for write_node in write_nodes:
        write_name = write_node.name()
        title = f"Nuke Render: {os.path.basename(script_path)} - {write_name}"

        job = tq.Job(title=title, priority=100)

        cmd = [
            "nuke.exe", "-x", script_path,
            "-F", f"{first_frame}-{last_frame}",
            "-X", write_name
        ]

        task = tq.Task(title=f"Render {write_name}", argv=cmd)
        job.addChild(task)

        try:
            tq.spool(job)
            nuke.message(f"Submitted {title} to Tractor.")
        except Exception as e:
            nuke.message(f"Submission failed: {e}") 