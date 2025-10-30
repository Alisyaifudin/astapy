"""Utility module to printout stream to stdout"""
import sys
import subprocess
import time

def stream_cmd(cmd, log: bool):
    '''stream cmd stdout to python stdout'''
    print("Running:", " ".join(cmd))

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    stdout = process.stdout
    if stdout is None:
        raise IOError("No stdout")
    if log:
        try:
            while process.poll() is None:  # process still running
                # read whatever is available without blocking indefinitely
                chunk = ""
                start = time.time()
                while True:
                    b = stdout.read(1)
                    chunk += b
                    if chunk == "":
                        break
                    now = time.time()
                    if now - start > 0.1:
                        break
                sys.stdout.write(chunk)
                sys.stdout.flush()

            remainder = stdout.read()
            if remainder:
                print(remainder, end="", flush=True)
        except KeyboardInterrupt:
            print("Interrupted by user, terminating ASTAP...")
            process.terminate()
            raise
