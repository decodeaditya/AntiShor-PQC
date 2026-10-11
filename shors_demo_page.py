import streamlit as st
from functions.function_shors import crack_rsa
import time

st.set_page_config(
    page_title="Shor's Algorithm Simulator",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Simulating Shor’s Algorithm")

st.markdown(
    """
    Shor’s algorithm shows how a sufficiently large quantum computer could break widely used public-key
    cryptography, such as RSA, by factoring large numbers efficiently.

    This demo simulates the main idea: find the repeating pattern, or **period**, of a modular function.
    That period can then be used to find the prime factors of public key.
    """
)

st.sidebar.header("Choose a target number")

def reset_simulation_state():
    keys_to_clear = [
        "history_df",
        "random_num",
        "period",
        "simulation_done",
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

key_to_factor = st.sidebar.selectbox(
    "Number to factor (N = p × q):",
    options=[35, 24, 77, 143, 221, 3233],
    index=0,
    on_change=reset_simulation_state,
    help="Each option is a small number that can be factored into two primes.",
)

st.sidebar.caption(
    """
Options are given so that classical computers don't crash while factoring. 
At the end it's Simulation not real QPU, but Pattern is almost same in real Quantum computers.
"""
)

st.sidebar.divider()

st.sidebar.caption(
    "This app simulates the mathematical behaviour behind Shor’s algorithm. "
    "It does not run on an actual quantum computer."
)

with st.expander("How Shor’s algorithm works? See here"):
    st.markdown(
        """
        ### The goal

        We choose a number `N` that is the product of two prime numbers (Public Key):

        ```text
        N = p × q
        ```

        For example:

        ```text
        15 = 3 × 5
        ```

        In RSA-style cryptography, factoring a very large `N` is extremely difficult for classical computers.

        Breaking Encryption using Shor's algorithm uses a hybrid approach: a classical and quantum computer working together.

        * **Note:** We never use even numbered Keys in RSA cryptography because it can be solved immediately by dividing by 2. (I just included a even number just for demo in dropdown)

        Suppose `N = 24` 
        ```text
        So one factor is 2, 
        and other one is 24/2 = 12
        ```

        Moving to main part, Shor’s algorithm first chooses a random number `a`, where:

        ```text
        1 < a < N
        ```

        * Suppose `a` shares a factor with `N`, we can find a factor immediately using the greatest common divisor:
        
        ```text
        gcd(a, N)
        ```
        Example: If `N = 15` and we choose `a = 3`, then:

        ```text
        gcd(3, 15) = 3
        and other factor is 15/3 = 5
        ```

        * Otherwise, we study this repeating function:

        ```text
        f(r) = a^r mod N
        ```

        This is only part for which Quantum computers are needed, that is to study the repeating pattern of this modular function.
        
        Example: If `N = 15` and we choose `a = 7`, then:

        ```text
        f(0) = 7^0 mod 15 = 1
        f(1) = 7^1 mod 15 = 7
        f(2) = 7^2 mod 15 = 4
        f(3) = 7^3 mod 15 = 13      
        f(4) = 7^4 mod 15 = 1
        ```
        Observe that the function repeats every 4 steps, so the period is `r = 4`.

        A quantum computer can use period-finding to estimate how often this function repeats.

        If the period is `r`, Shor’s algorithm uses:

        ```text
        a^(r/2) ± 1
        ```

        So for `N = 15` and `a = 7`, we have `r = 4`, so we compute:

        ```text
        7^(4/2) - 1 = 48
        7^(4/2) + 1 = 50
        ```

        and calculates:

        ```text
        gcd(a^(r/2) - 1, N)
        gcd(a^(r/2) + 1, N)
        ```

        for example, we can compute:

        ```text
        gcd(48, 15) = 3
        gcd(50, 15) = 5
        ```

        These calculations often reveal the two prime factors of `N`.
        """
    )


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Number to factor: {key_to_factor}")

    if st.button(
        "Start simulation",
        type="primary",
        width='stretch',
    ):
        with st.spinner("Running Shor’s algorithm simulation..."):
            start_time = time.time()

            fact1, fact2, period, random_num, periodic_wave = crack_rsa(
                key_to_factor
            )

            elapsed = time.time() - start_time

        if fact1 and fact2:
            st.success("Factors found successfully.")

            st.session_state["simulation_done"] = True

            # Case 1: N was even, so no quantum period-finding was needed
            if not random_num:
                st.warning(
                    """The selected number is even, so one factor is immediately 2. 
                    No quantum period-finding was needed."""
                )

                factor_col1, factor_col2 = st.columns(2)

                factor_col1.metric("Factor 1", fact1)
                factor_col2.metric("Factor 2", fact2)

                st.metric("Time taken", f"{elapsed:.4f} s")

            else:
                st.metric("Random number chosen (a)", random_num)

                if period:
                    st.metric("Period found (r)", period)
                else:
                    st.warning(
                        """A factor was found directly because the chosen random number 
                        shares a factor with N. Quantum period-finding was not needed."""
                    )

                factor_col1, factor_col2 = st.columns(2)

                factor_col1.metric("Factor 1", fact1)
                factor_col2.metric("Factor 2", fact2)

                st.metric("Time taken", f"{elapsed:.4f} s")

                st.session_state["history_df"] = periodic_wave
                st.session_state["random_num"] = random_num
                st.session_state["period"] = period

        else:
            st.error(
                "The simulation could not find a valid period. Try running it again."
            )


with col2:
    st.subheader("Quantum periodicity wave")

    if (
        "history_df" in st.session_state
        and st.session_state["history_df"] is not None
    ):
        df = st.session_state["history_df"]
        random_num = st.session_state["random_num"]
        period = st.session_state["period"]

        st.markdown(
            f"""
            The quantum part of Shor’s algorithm studies the repeating pattern of:

            $$f(r) = {random_num}^r \\pmod{{{key_to_factor}}}$$
            """
        )

        st.line_chart(
            df.set_index("Power (r)")["Remainder"],
            height=300,
        )

        st.success(
            f"""
            **Notice:** the remainders repeat after every **{period}** steps.

            This repeating structure is the period that Shor’s algorithm tries to find.
            Once we know the period, classical post-processing using GCD can recover the factors.
            """
        )

    elif st.session_state.get("simulation_done") and (
        not st.session_state.get("random_num")
        or not st.session_state.get("period")
    ):
        st.warning(
            "The factors were found without quantum period-finding, so there is no "
            "periodicity wave to display."
        )

    else:
        st.info(
            "Run the simulation to generate and visualize the periodicity data."
        )


