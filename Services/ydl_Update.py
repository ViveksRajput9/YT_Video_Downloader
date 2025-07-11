import subprocess
import sys

class YtDlpUpdater:
    @staticmethod
    def check_and_update():
        """Check if yt-dlp is installed and update it if necessary."""
        try:
            package_name = "yt-dlp"

            # Check if yt-dlp is installed
            print(f"Checking if {package_name} is installed...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                stdout=subprocess.PIPE,
                text=True
            )

            if f"Name: {package_name}" in result.stdout:
                print(f"{package_name} is installed. Checking for updates...")

                # Attempt to update yt-dlp
                update_process = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", package_name],
                    stdout=subprocess.PIPE,
                    text=True
                )

                # Check if it's already up-to-date or successfully updated
                if "Requirement already satisfied" in update_process.stdout:
                    print(f"{package_name} is already up-to-date.")
                else:
                    print(f"{package_name} updated successfully!")
            else:
                print(f"{package_name} is not installed. Installing now...")

                # Install yt-dlp
                subprocess.run([sys.executable, "-m", "pip", "install", package_name])
                print(f"{package_name} installed successfully!")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Terminate the process after checking
            sys.exit()

# Use the static method without creating an instance
if __name__ == "__main__":
    YtDlpUpdater.check_and_update()
