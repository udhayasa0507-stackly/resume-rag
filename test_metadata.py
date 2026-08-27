from src.fs_tools import read_file
from src.metadata import extract_metadata


result = read_file("resumes/arun_kumar.txt")

if not result["success"]:
    print("Error:", result["error"])
    exit()


metadata = extract_metadata(result["text"])


print("\nExtracted Metadata")
print("=" * 50)

print("Candidate Name:")
print(metadata["candidate_name"])

print("\nSkills:")
print(metadata["skills"])

print("\nExperience Years:")
print(metadata["experience_years"])

print("\nEducation:")
print(metadata["education"])