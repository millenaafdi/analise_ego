import streamlit as st
import matplotlib.pyplot as plt

# --- Egograma ---
st.title("🧠 Autoavaliação de Egograma")

perguntas_egograma = {
    "Pai Crítico": [
        "Eu costumo corrigir os outros quando acho que estão errados.",
        "Eu sou exigente comigo e com os outros.",
        "Tenho regras bem definidas sobre o que é certo e errado."
    ],
    "Pai Nutritivo": [
        "Gosto de cuidar das pessoas ao meu redor.",
        "Costumo escutar e apoiar quem precisa.",
        "Me preocupo com o bem-estar dos outros."
    ],
    "Adulto": [
        "Tomo decisões com base em fatos e lógica.",
        "Consigo manter a calma mesmo em situações difíceis.",
        "Analiso bem antes de agir."
    ],
    "Criança Livre": [
        "Gosto de me divertir sem me preocupar com julgamentos.",
        "Sou criativo(a) e espontâneo(a).",
        "Expresso minhas emoções livremente."
    ],
    "Criança Adaptada": [
        "Costumo seguir regras para evitar problemas.",
        "Me preocupo com o que os outros pensam de mim.",
        "Às vezes me sinto inseguro(a) em expressar minhas opiniões."
    ]
}

pontuacoes_egograma = {}

for estado, questoes in perguntas_egograma.items():
    total = 0
    st.subheader(estado)
    for q in questoes:
        total += st.slider(q, 1, 5, 3, key=q)
    pontuacoes_egograma[estado] = total

if st.button("📊 Ver resultado do Egograma"):
    st.subheader("Resultado do Egograma")
    for estado, valor in pontuacoes_egograma.items():
        st.markdown(f"**{estado}**: {valor} pontos")

    fig, ax = plt.subplots()
    ax.bar(pontuacoes_egograma.keys(), pontuacoes_egograma.values(),
           color=['red', 'orange', 'gray', 'green', 'blue'])
    ax.set_title("Egograma - Perfil dos Estados do Ego")
    ax.set_xlabel("Estados do Ego")
    ax.set_ylabel("Pontuação")
    st.pyplot(fig)

# --- Triângulo Dramático Tradicional ---
st.title("🎭 Teste do Triângulo Dramático (tradicional)")

td_perguntas = {
    "Vítima": [
        "Sinto que as pessoas não me compreendem.",
        "Muitas vezes me sinto injustiçado(a).",
        "Tenho dificuldade de agir por conta própria em certas situações."
    ],
    "Salvador": [
        "Costumo ajudar mesmo quando não sou solicitado(a).",
        "Sinto que devo resolver os problemas dos outros.",
        "Me preocupo em excesso com o bem-estar alheio."
    ],
    "Perseguidor": [
        "Costumo criticar quem não age como eu espero.",
        "Acho que certas pessoas merecem ser repreendidas.",
        "Me irrito com facilidade quando algo está errado."
    ]
}

td_pontuacoes = {}

for papel, questoes in td_perguntas.items():
    total = 0
    st.subheader(papel)
    for q in questoes:
        total += st.slider(q, 1, 5, 3, key=f"td_{q}")
    td_pontuacoes[papel] = total

if st.button("🔎 Ver resultado do Triângulo Dramático Tradicional"):
    st.subheader("Resultado do Triângulo Dramático (tradicional)")
    for papel, valor in td_pontuacoes.items():
        st.markdown(f"**{papel}**: {valor} pontos")
        if valor >= 13:
            st.warning(f"Você se identifica fortemente com o papel de **{papel}**.")
        elif valor >= 9:
            st.info(f"Você demonstra algumas características do papel de **{papel}**.")
        else:
            st.success(f"Pouca tendência ao papel de **{papel}**.")

    fig2, ax2 = plt.subplots()
    ax2.bar(td_pontuacoes.keys(), td_pontuacoes.values(),
            color=['purple', 'cyan', 'brown'])
    ax2.set_title("Triângulo Dramático - Papéis Psicológicos")
    ax2.set_xlabel("Papéis")
    ax2.set_ylabel("Pontuação")
    st.pyplot(fig2)

# --- Triângulo Dramático com Perguntas Situacionais ---
st.title("🎭 Teste do Triângulo Dramático (Perguntas Situacionais)")

td_perguntas_situacionais = {
    "Vítima": [
        "Você prefere esperar que alguém resolva por você, em vez de pedir ajuda diretamente?",
        "Sente-se injustiçado quando criticado e pensa 'ninguém me entende'?",
        "Quando algo dá errado fora do seu controle, você pensa 'isso sempre acontece comigo'?"
    ],
    "Salvador": [
        "Você ajuda alguém estressado sem que a pessoa peça, mesmo estando ocupado(a)?",
        "Resolve problemas dos outros para se sentir útil, mesmo se sobrecarregando?",
        "Pensa em soluções antes mesmo de perguntar se querem sua ajuda?"
    ],
    "Perseguidor": [
        "Você aponta erros dos outros imediatamente e espera mudanças no comportamento?",
        "Já criticou alguém dizendo 'você sempre faz isso errado'?",
        "Sente o impulso de corrigir falhas alheias, mesmo sem ser pedido?"
    ]
}

td_pontuacoes_situacionais = {}

for papel, questoes in td_perguntas_situacionais.items():
    total = 0
    st.subheader(f"{papel} (situacional)")
    for q in questoes:
        total += st.slider(q, 1, 5, 3, key=f"td_sit_{q}")
    td_pontuacoes_situacionais[papel] = total

if st.button("📌 Ver resultado do Triângulo Dramático Situacional"):
    st.subheader("Resultado do Triângulo Dramático (Situacional)")
    for papel, valor in td_pontuacoes_situacionais.items():
        st.markdown(f"**{papel}**: {valor} pontos")
        if valor >= 13:
            st.warning(f"Você frequentemente assume o papel de **{papel}** em situações reais.")
        elif valor >= 9:
            st.info(f"Você apresenta algumas tendências ao papel de **{papel}** em seu comportamento.")
        else:
            st.success(f"Baixa tendência a se posicionar como **{papel}**.")

    fig3, ax3 = plt.subplots()
    ax3.bar(td_pontuacoes_situacionais.keys(), td_pontuacoes_situacionais.values(),
            color=['#9932CC', '#00CED1', '#A52A2A'])
    ax3.set_title("Triângulo Dramático - Situações Reais")
    ax3.set_xlabel("Papéis")
    ax3.set_ylabel("Pontuação")
    st.pyplot(fig3)

