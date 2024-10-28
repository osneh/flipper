import os, glob 

##cmd = "/group/picmic/RUNDATA/TCPdataB/run_vrefn*_vrefp*/sampic_ru*/picmic_dat*/picmic_*.bin"
##
##print(cmd)
##print(40*'--')
##
##os.system('ls '+cmd)

print(40*'--')

def find_files(base_dir):
	# Construct the search pattern
	search_pattern = os.path.join(base_dir,"run_vrefn*_vrefp*","sampic_ru*","picmic_dat*","picmic_*.bin")

	# Use glob to find all matching files
	mfiles = glob.glob(search_pattern,recursive=True)
	
	return mfiles

##matching_files = find_files()

# Example usage for both Linux and Windows:
if __name__ == "__main__":
    # Replace with the correct base directory path for your system
    base_directory_linux = '/group/picmic/RUNDATA/TCPdataB/'
    base_directory_windows = r'K:\RUNDATA\TCPdataB'  # Example Windows path
    
    # Use the correct base directory depending on the platform
    if os.name == 'nt':  # If on Windows
        base_directory = base_directory_windows
    else:  # If on Linux
        base_directory = base_directory_linux
    
    # Find matching files
    matching_files = find_files(base_directory)
    
    # Print the list of files found
    for file in matching_files:
        print(file)
