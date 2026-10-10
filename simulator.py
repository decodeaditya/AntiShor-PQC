# importing needed modules
import random
import math 
import pandas as pd

def simulate_finding_period(key_to_factor: int, random_num: int):

    '''It simulates the quantum part of Shor's algorithm to find periodicity of  key using random number.

    Args:
        key_to_factor (int):  key that needs to be decrypted.
        random_num (int): Random number used to find periodicity of Key.

    Returns:
        period (int): After finding out which power raised to random number give modulus of  key and start to repeat again.
    '''

    periodic_wave = []
    r_found = 0

    for r in range(1, min(key_to_factor * 2, 5000)):
        value = pow(random_num, r, key_to_factor)
        periodic_wave.append({'Power (r)':r, 'Remainder':value})
        if value == 1 and r_found == 0:
            r_found = r

    return r_found, pd.DataFrame(periodic_wave)

def crack_rsa(key_to_factor: int):
    '''This function will simulate Shor's algorithm to factor the key.

    Args: 
        key_to_factor (int): Key that needs to be decrypted.

    Returns:
        tuple: A tuple having the two factors of the key, periodicity and the random number used. (factor1, factor2, period, random_num)
    '''

    '''
    There will be 3 cases to find factors of key to factor:
    Case 1. If key is even, we can immediately return 2 and key_to_factor//2 as factors.
    Case 2. If random number is factor of key, we don't need quantum part to calculate factors since it straight away gives 2 factors.
    Case 3. If the random number and  key are co-prime, we will use quantum part to find periodicity then use it to find factors. (Only case where quantum computing is used)

    Some notes:
        1. Checking if key is even, because even numbers are easy to factor using classical computing menthods. 
        Therefore they are not used in Encryption. Mostly semi primes which are harder to factor are used in Encryption.

        2. Random number is used to find periodicity of the key. This is the quantum part of the algorithm.

        3. In this simulation, we are not using any quantum computing libraries. We are just simulating the steps of Shor's algorithm to find factors of  key.
    '''


    # [Case 1] 
    if (key_to_factor & 1 == 0): # Bitwise version for key_to_factor % 2 == 0
        return 2, key_to_factor//2, None, None, None

    attempts = 0 
    max_attempts = 22 # max attempts to find factors of  key
    while attempts < max_attempts: # Only 22 attempts are made to find factors
        random_num = random.randint(2, key_to_factor - 1)

        # [Case 2]
        if (math.gcd(random_num, key_to_factor) > 1):
            return math.gcd(random_num, key_to_factor), key_to_factor // math.gcd(random_num, key_to_factor), None, random_num, None

        # [Case 3]
        if (math.gcd(key_to_factor, random_num) == 1):

            # Finding periodicity of  key using random number. This is the quantum part of the algorithm.
            period, periodicWave = simulate_finding_period(key_to_factor, random_num)

            if period & 1 == 0 and period != 0: # Checking if period is even and non zero, otherwise we can't find factors of  key
                guessedFactor1 = math.gcd(pow(random_num, period // 2) - 1, key_to_factor)
                guessedFactor2 = math.gcd(pow(random_num, period // 2) + 1, key_to_factor)

                if guessedFactor1 > 1 and guessedFactor2 > 1 and guessedFactor1 * guessedFactor2 == key_to_factor: # Checking if  we are not returning same  key as one of factors and validating that the factors are correct
                    return guessedFactor1, guessedFactor2, period, random_num, periodicWave

        attempts += 1

    raise ValueError(f'Failed to factor {key_to_factor} after {max_attempts} attempts. Exiting...')

