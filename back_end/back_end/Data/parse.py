import pandas as pd


npi_table = pd.read_csv("C:\\Users\\vpk12\\OneDrive\\Desktop\\CS340\\final\\Baymax\\back_end\\back_end\\Data\\npidata_pfile_20230918-20230924.csv")

columns_to_drop = ['NPI Deactivation Reason Code', 'NPI Deactivation Date', 'Replacement NPI', 'NPI Reactivation Date', 'Provider Gender Code']

# List comprehensions for each set of column names
columns_to_drop += [f"Other Provider Identifier_{i}" for i in range(1, 51)]
columns_to_drop += [f"Other Provider Identifier Type Code_{i}" for i in range(1, 51)]
columns_to_drop += [f"Other Provider Identifier State_{i}" for i in range(1, 51)]
columns_to_drop += [f"Other Provider Identifier Issuer_{i}" for i in range(1, 51)]
columns_to_drop += [f"Healthcare Provider Primary Taxonomy Switch_{i}" for i in range(4, 16)]
columns_to_drop += [f"Provider License Number_{i}" for i in range(4, 16)]
columns_to_drop += [f"Provider License Number State Code_{i}" for i in range(4, 16)]
columns_to_drop += [f"Healthcare Provider Taxonomy Code_{i}" for i in range(4, 16)]
columns_to_drop += [f"Healthcare Provider Taxonomy Group_{i}" for i in range(4, 16)]
columns_to_drop += [f"Healthcare Provider Primary Taxonomy Switch_{i}" for i in range(4, 16)]

npi_table = npi_table.drop(columns=columns_to_drop)

npi_table['Name'] = npi_table['Provider Organization Name (Legal Business Name)']

full_name = npi_table['Provider Name Prefix Text'].str.cat([
    npi_table['Provider First Name'],
    npi_table['Provider Middle Name'],
    npi_table['Provider Last Name (Legal Name)'],
    npi_table['Provider Name Suffix Text']
], sep=' ', na_rep='').str.strip()

# Fill NaN values in 'Name' column with the created full name
npi_table['Name'] = npi_table['Name'].fillna(full_name)

columns_to_drop = ['Provider Organization Name (Legal Business Name)', 
              'Provider Last Name (Legal Name)', 
              'Provider Name Prefix Text',
              'Provider First Name',
              'Provider Middle Name',
              'Provider Name Suffix Text',
              'Provider Other Organization Name',
              'Provider Other Organization Name Type Code',
              'Provider Other Last Name',
              'Provider Other First Name',
              'Provider Other Middle Name',
              'Provider Other Name Prefix Text',
              'Provider Other Name Suffix Text',
              'Provider Other Credential Text',
              'Provider Other Last Name Type Code']

npi_table = npi_table.drop(columns=columns_to_drop)

mailing_address = npi_table['Provider First Line Business Mailing Address'].str.cat([
    npi_table['Provider Second Line Business Mailing Address']], sep=' ', na_rep='').str.strip()
columns_to_drop = npi_table.filter(like="Address").columns
npi_table = npi_table.drop(columns=columns_to_drop)

npi_table['Mailing Address'] = mailing_address

auth_full_name = npi_table['Authorized Official Name Prefix Text'].str.cat([
    npi_table['Authorized Official First Name'],
    npi_table['Authorized Official Middle Name'],
    npi_table['Authorized Official Last Name'],
    npi_table['Authorized Official Name Suffix Text']
], sep=' ', na_rep='').str.strip()

columns_to_drop = ['Authorized Official Last Name', 
                   'Authorized Official First Name', 
                   'Authorized Official Middle Name', 
                   'Authorized Official Name Prefix Text', 
                   'Authorized Official Name Suffix Text']
npi_table = npi_table.drop(columns=columns_to_drop)
npi_table['Authorized Official Name'] = npi_table['Name'].fillna(full_name)

npi_table.to_csv('parsed_npidata.csv', index=False)
