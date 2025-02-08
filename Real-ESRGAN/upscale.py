import os
import subprocess

# Clone and set up the Real-ESRGAN repository if not already present
if not os.path.exists("Real-ESRGAN"):
    subprocess.run(["git", "clone", "https://github.com/xinntao/Real-ESRGAN.git"])

repo_path = os.path.abspath("Real-ESRGAN")
os.chdir(repo_path)

# Install dependencies
subprocess.run(["pip", "install", "-r", "requirements.txt"])
subprocess.run(["python", "setup.py", "develop"])

# Fix potential issue in basicsr degradations.py
# The import path may have changed in newer versions of torchvision

degradations_path = os.path.join(repo_path, "basicsr", "data", "degradations.py")
if os.path.exists(degradations_path):
    with open(degradations_path, "r") as file:
        file_data = file.readlines()
    
    for i, line in enumerate(file_data):
        if 'from torchvision.transforms.functional_tensor import rgb_to_grayscale' in line:
            file_data[i] = 'from torchvision.transforms.functional import rgb_to_grayscale\n'
            break
    
    with open(degradations_path, "w") as file:
        file.writelines(file_data)
    print("Fix applied to basicsr degradations.py.")

# Configuration
source = "video"  # Options: "image" or "video"
input_path = os.path.join(repo_path, "inputs", "video_540p.mp4")  # Change this to your input file
model = "RealESRGAN_x4plus"  # Select the model
scale = 2  # Upscale factor
face_enhance = False  # Enable face enhancement (for images with faces)

# Generate output paths
def generate_output_path(input_path):
    return os.path.dirname(input_path)

def generate_result_path(input_path):
    directory, filename = os.path.split(input_path)
    filename_without_ext, ext = os.path.splitext(filename)
    return os.path.join(directory, f"{filename_without_ext}_out{ext}")

output = generate_output_path(input_path)
result = generate_result_path(input_path)

print(f"Output directory: {output}")
print(f"Result file: {result}")

# Construct the inference command
code = "inference_realesrgan_video.py" if source == "video" else "inference_realesrgan.py"
command = [
    "python", code,
    "-i", input_path,
    "-n", model,
    "-o", output,
    "-s", str(scale)
]
if face_enhance:
    command.append("--face_enhance")

# Run Real-ESRGAN
subprocess.run(command)

print(f"Processing complete. Your output file is available at: {result}")
