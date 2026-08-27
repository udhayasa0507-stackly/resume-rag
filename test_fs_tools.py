from src.fs_tools import read_file


result = read_file("resumes/test_resume.txt")

if result["success"]:
    print("\nFile loaded successfully")
    print("Filename:", result["filename"])
    print("File type:", result["file_type"])
    print("Character count:", result["character_count"])

    print("\nExtracted text:")
    print("-" * 50)
    print(result["text"])
    print("-" * 50)

else:
    print("Error:", result["error"])