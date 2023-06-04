import csv
 # Read the H-Index list
with open('HIndexList.tsv', 'r') as hindex_file:
    hindex_reader = csv.reader(hindex_file, delimiter='\t')
    hindex_list = [row[0] for row in hindex_reader]
 # Open the input files
with open('GSCHOLARresults.tsv', 'r') as gscholar_file, \
     open('WOSPublonsResults.tsv', 'r') as wos_file, \
     open('SCOPUSresults.tsv', 'r') as scopus_file:
     # Create CSV readers for each file
    gscholar_reader = csv.reader(gscholar_file, delimiter='\t')
    wos_reader = csv.reader(wos_file, delimiter='\t')
    scopus_reader = csv.reader(scopus_file, delimiter='\t')
     # Open the output file
    with open('ComperHindexlistResults.tsv', 'w', newline='') as output_file:
        # Create a CSV writer
        writer = csv.writer(output_file, delimiter='\t')
         # Write the header row to the output file
        writer.writerow(['GoogleID', 'ScopusID', 'WOSID', 'media_h_index'])
         # Initialize variables for calculating the media H-Index
        total_h_index = 0
        count = 0
         # Loop over the H-Index list
        for h_index in hindex_list:
            # Initialize variables for storing the IDs and H-Index
            google_id = ''
            scopus_id = ''
            wos_id = ''
            h_index_list = []
             # Search for the H-Index in the Google Scholar file
            for row in gscholar_reader:
                if row[1] == h_index:
                    google_id = row[0]
                    h_index_list.append(int(row[1]))
                    break
             # Reset the reader
            gscholar_file.seek(0)
            next(gscholar_reader)
             # Search for the H-Index in the WOS file
            for row in wos_reader:
                if row[1] == h_index:
                    wos_id = row[0]
                    h_index_list.append(int(row[1]))
                    break
             # Reset the reader
            wos_file.seek(0)
            next(wos_reader)
             # Search for the H-Index in the Scopus file
            for row in scopus_reader:
                if row[1] == h_index:
                    scopus_id = row[0]
                    h_index_list.append(int(row[1]))
                    break
             # Reset the reader
            scopus_file.seek(0)
            next(scopus_reader)
             # Calculate the media H-Index
            media_h_index = sum(h_index_list) / len(h_index_list)
             # Write the IDs and media H-Index to the output file
            writer.writerow([google_id, scopus_id, wos_id, media_h_index])
             # Update the total H-Index and count
            total_h_index += media_h_index
            count += 1
         # Calculate the media H-Index for the entire list
        media_h_index = total_h_index / count
         # Write the media H-Index to the output file
        writer.writerow([])
        writer.writerow(['Media H-Index', '', '', media_h_index])