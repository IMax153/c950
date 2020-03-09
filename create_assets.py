#!/usr/bin/env python3

import json
import numpy as np
import os
import pandas as pd
import pathlib
import re
import time

# Open Excel workbooks
distance_df = pd.read_excel(
    io='.raw/wgups_distance_data.xlsx',
    skiprows=7,
    usecols='C:AC'
)
package_df = pd.read_excel(
    io='.raw/wgups_package_data.xlsx',
    skiprows=7,
    names=['id', 'address', 'city', 'state',
           'zip', 'deadline', 'kg', 'notes']
)


def create_matrix(df):
    """
    Creates a symmetric matrix from the specified dataframe.
    """
    matrix = df.transpose().to_numpy()
    il = np.tril_indices(len(df), -1)
    matrix[il] = matrix.T[il]
    return matrix


def format_address(address):
    """
    Formats the specified address string to include only the street number and street address.
    """
    return re.search(r'(\d+\s*\w+\s*\w+\s*\w+)', address).group()


def format_deadline(deadline):
    """
    Formats the specified deadline to HH:MM on a 24 hour clock.
    """
    return '17:00' if deadline == 'EOD' else f'{deadline.hour:02}:{deadline.minute:02}'


def create_distance_data(df):
    """
    Builds a dictonary that lists the distance in miles from an address to all other addresses
    that must be visited by the WGUPS.
    """
    distance_data = {}
    addresses = [format_address(x.split('\n')[1]) for x in df.columns]
    distance_matrix = create_matrix(df)

    for i, from_address in enumerate(addresses):
        for j, to_address in enumerate(addresses):
            miles = distance_matrix[j, i]

            if from_address in distance_data:
                distance_data[from_address][to_address] = miles
            else:
                distance_data[from_address] = {}
                distance_data[from_address][to_address] = miles

    return distance_data


def create_package_data(df):
    """
    Builds a dictionary that lists the information for each package by package identifier.
    """
    packages = {}
    rows = df.to_dict('records')

    # Create a package entry for each row
    for row in rows:
        # Create package
        package = {k: row[k] for k in ('id', 'city', 'state', 'zip', 'kg')}

        # Format package address
        package['address'] = format_address(row['address'])

        # Format package deadline
        package['deadline'] = format_deadline(row['deadline'])

        # Handle package restrictions
        notes = str.lower(row['notes'] if not row['notes'] is np.nan else '')
        package['required_truck'] = 2 if 'can' in notes else False
        package['is_peer'] = True if 'must' in notes else False
        package['is_delayed'] = True if 'delayed' in notes else False

        # Add package to the package dictionary
        packages[package['id']] = package

    return packages


# Create the address data file
with open('wgups/data/data/distance_data.json', 'w') as outfile:
    distance_data = create_distance_data(distance_df)
    json.dump(distance_data, outfile, indent=2)

# Create the package data
with open('wgups/data/data/package_data.json', 'w') as outfile:
    package_data = create_package_data(package_df)
    json.dump(package_data, outfile, indent=2)
