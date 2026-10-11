import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Post-Quantum Cryptography Simulation",
    page_icon="🔏",
    layout="wide",
)

st.title("🔏 Glimpse of Post-Quantum Cryptography")

st.markdown(
    """
    Many encryption like RSA and ECC used today rely on mathematical complexity that quantum computers could solve much faster than 
    classical computers by finding the patterns.

    **Post-quantum cryptography** means to build type of encryption that remains secure against powerful
    quantum computers. One of the popular approach is **lattice-based cryptography**, and one of its core ideas is
    **Learning With Errors (LWE)**.

    This demo shows the basic intuition behind LWE: hide a secret key inside noisy mathematical equations.
    """
)

st.sidebar.header("Parameters")

secret_value = st.sidebar.slider(
    "Secret key (s)",
    min_value=0,
    max_value=100,
    value=22,
    help="The secret key we want to protect.",
)

modulus_q = st.sidebar.number_input(
    "Modulus (q)",
    min_value=97,
    max_value=997,
    value=101,
    step=10,
    help="All calculations wrap around this value.",
)

noise_level = st.sidebar.slider(
    "Noise level (max e)",
    min_value=0,
    max_value=20,
    value=4,
    help="Random errors added to hide the secret.",
)

num_equations = st.sidebar.slider(
    "Number of public equations",
    min_value=5,
    max_value=30,
    value=15,
    help="How many noisy public keys.",
)

if st.sidebar.button("Generate public key"):
    st.session_state["seed_val"] = np.random.randint(0, 1_000_000)

seed = st.session_state.get("seed_val", 4)
rng = np.random.default_rng(seed)

with st.expander("How this Demo works? (See Here)"):
    st.markdown(
        """
        ### The story

        Imagine that Kasumi has a secret number `s` which she never shares directly.

        Instead, she publishes several equations of this form:

        ```text
        b = (a × s + e) mod q
        ```

        Here:

        - `a` is a public random value.
        - `s` is Kasumi’s secret.
        - `e` is small random noise.
        - `q` is the modulus.
        - `b` is the public output.

        ### Why the noise matters?

        So, this is not something new. The main aim of both Tradtional and Post Quantum Cryptography is to hide the secret key and wrap it up into Public keys
        which can be used to communicate with other parties. But since quantum computers poses a threat to how we Traditionaly encrypt our keys, we need to use new methods to wrap our secret keys into public keys. 
        Its basically a new way to hide the secret key into public keys.

        By adding noise, we are making patterns less obvious, so quantum computer's power of fast computation is not enough to find and break patterns.
        Without noise, an attacker could look at the public equations and recover `s`.

        With noise, the relationship between `a` and `b` becomes unclear. The attacker sees noisy data and
        cannot easily tell which secret value produced it.

        ### Remember

        This is a simplified, single-number version of LWE for learning purposes.

        Real lattice-based encryptions use vectors, larger parameters, and carefully chosen noise distributions.
        They are designed to resist attacks from both classical and quantum computers.
        """
    )


a_values = rng.integers(0, modulus_q, size=num_equations)
errors = rng.integers(-noise_level, noise_level + 1, size=num_equations)

b_exact = (a_values * secret_value) % modulus_q
b_noisy = (a_values * secret_value + errors) % modulus_q

df = pd.DataFrame(
    {
        "Equation Index": [f"Eq {i + 1}" for i in range(num_equations)],
        "Public Value (a)": a_values,
        "Perfect Output (a × s) mod q": b_exact,
        "Added Noise (e)": errors,
        "Noisy Public Output (b)": b_noisy,
    }
)

st.subheader("Try the simulation")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Public key Generation")

    st.markdown(
        "`a`, `b` and `modulus_q` are always public. The secret `s` and the exact noise values stay hidden."
    )

    st.info(f"Public equation: `b = (a × s + e) mod {modulus_q}`")

    public_table = df[
        [
            "Equation Index",
            "Public Value (a)",
            "Added Noise (e)",
            "Noisy Public Output (b)",
        ]
    ]

    st.dataframe(
        public_table,
        width='stretch',
        hide_index=True,
    )

with col2:
    st.markdown("### What an attacker sees")

    st.markdown(
        "An attacker only sees the public data `(a, b)`. The noise makes the underlying pattern hard to recognize."
    )

    graph_data = pd.DataFrame(
        {
            "Public Value (a)": a_values,
            "Noisy Public Output (b)": b_noisy,
        }
    )

    st.scatter_chart(
        graph_data,
        x="Public Value (a)",
        y="Noisy Public Output (b)",
        color="#ABFF4B",
        size=100,
        width='stretch',
        height=420,
    )

st.success(
    """
    **You can try this:** set **Noise level** to `0` and look at the chart. Then increase it.

    You will notice that without noise, the outputs follow a clearer mathematical structure. As noise increases, that structure becomes
    harder to see — this is the basic intuition behind Learning With Errors.
    """
)

st.divider()

st.caption(
    "This is just simulation of the core idea behind Learning With Errors (LWE), a real cryptographic implementation is more complex and use vectors and matrices instead of linear algebra."
)


