import streamlit as st
from simulator import crack_rsa
import time 

st.set_page_config(page_title="Shor's Algorithm QPU Simulator", page_icon="🛡️", layout="wide")

st.title("🛡️ Simulating Shor’s Algorithm")
st.markdown("Shor’s algorithm shows how a sufficiently large quantum computer can shatter modern public-key cryptography by turning period-finding into factoring.") 

def reset_simulation_state():
    keys_to_clear = ['history_df', 'random_num', 'period', 'simulation_done']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

#sidebar
st.sidebar.header("Select Target")
key_to_factor = st.sidebar.selectbox(
    "Choose a example Key (N = p × q):",
    options=[35,24, 77, 143, 221, 3233],
    on_change=reset_simulation_state,
    index=2,
    help="These are products of two secret prime numbers. Quantum computers factor them rapidly."
)

st.sidebar.caption("Options are given so that classical computers don't crash while factoring. At the end it's Simulation not real QPU, but Pattern is almost same in real Quantum computers.")
st.sidebar.markdown("---")
st.sidebar.header("How it works?")
st.sidebar.markdown(
    '''
    * Step 1: Choose a key. It is number whose factors are 2 prime numbers.

    * Step 2. A Random number is chosen between `2` and `key-1`. This random number is used to calculate periodicity of key. (This is part where Quantum computers are used)
    * Step 3: If random number is a factor of key, we can find factors without using Quantum computers. Classical computers can handle it.
    * Step 4: So after finding the periodicity of key, we can put it in by taking HCF of `(random_num^(period/2) ± 1)` and `Key`. You will find two prime factors of which can we easily simplified to find the secret prime numbers.
    ''')

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Key to Decrypt: {key_to_factor}")
    if st.button("Start Simulation", type="primary", use_container_width=True):
        with st.spinner("Starting simulation..."):
            start_time = time.time()
            fact1, fact2, period, random_num, periodic_wave = crack_rsa(key_to_factor)
            elapsed = time.time() - start_time

            if fact1 and fact2:
                st.success('Factors found Successfully')

                st.session_state['simulation_done'] =  True
                if not random_num:
                    st.warning('The Key was even, we have found factors and which was 2 and Key/2. No Quantum operation was needed. ')
                    sCol1, sCol2 = st.columns(2)
                    sCol1.metric('Factor 1', fact1)
                    sCol2.metric('Factor 2', fact2)

                    st.metric('Time Taken', f"{elapsed:.4f}s")

                else:
                    st.metric('Random number choosen', random_num)
                    
                    if period:
                        st.metric('Quantum Period found', period)
                    
                    else:
                        st.warning("Didn't need Quantum periodicity to find factors, Since random number was a factor of Key.")

                    sCol1, sCol2 = st.columns(2)
                    
                    sCol1.metric('Factor 1', fact1)
                    sCol2.metric('Factor 2', fact2)
                    
                    st.metric('Time Taken', f"{elapsed:.4f}s")

                    st.session_state['history_df'] = periodic_wave
                    st.session_state['random_num'] = random_num
                    st.session_state['period'] = period

            else:
                st.error("Quantum simulation timed out without finding a valid period. Try running it again!")

with col2:
    st.subheader("Quantum Periodicity Wave")
    if 'history_df' in st.session_state and st.session_state['history_df'] is not None:
        df = st.session_state['history_df']
        random_num = st.session_state['random_num']
        period = st.session_state['period']
    
        st.markdown(f"Quantum computers analyze the repeating periodicity of the function: \n$$f(r) = {random_num}^r \\pmod{{{key_to_factor}}}$$") 

        st.line_chart(df.set_index("Power (r)")["Remainder"], height=300)
        st.caption(f"The pattern perfectly repeats after every **{period} steps**. Classical systems either do guess or use brute force meanwhile quantum systems capture this entire wave shape instantly using Quantum parallelism.")
    

    elif st.session_state.get('simulation_done') and (not st.session_state.get('random_num') or not st.session_state.get('period')):
        st.warning('Since the factors were found instantly by the Classical computer, no Quantum period attempts were made.')

    else:
        st.info("Run simulation to generate and visualize the quantum periodicity data.")


