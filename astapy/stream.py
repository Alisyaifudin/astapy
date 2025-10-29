import sys
import subprocess
import time

def stream_cmd(cmd, log: bool):
    print("Running:", " ".join(cmd))

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    output = ""
    if log:
        try:
            while process.poll() is None:  # process still running
                # read whatever is available without blocking indefinitely
                chunk = ""
                start = time.time()
                while True:
                    b = process.stdout.read(1)
                    chunk += b
                    if chunk == "":
                        break
                    now = time.time()
                    if now - start > 0.1:
                        break
                sys.stdout.write(chunk)
                sys.stdout.flush()
                output+=chunk

            remainder = process.stdout.read()
            if remainder:
                print(remainder, end="", flush=True)
        except KeyboardInterrupt:
            print("Interrupted by user, terminating ASTAP...")
            process.terminate()
            raise
    else:
        output = process.stdout.read()
    return output[-1024:]