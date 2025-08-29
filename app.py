# app.py
import io
from datetime import datetime

import streamlit as st
import matplotlib.pyplot as plt

# Para o PDF (instale: pip install reportlab)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib import colors

st.set_page_config(page_title="Egograma & Triângulo Dramático", page_icon="🧠", layout="centered")

# =========================
# Utilidades
# =========================
def plot_egograma(scores: dict) -> io.BytesIO:
    """Gera o gráfico do Egograma e retorna como PNG em memória."""
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    ax.bar(scores.keys(), scores.values(), color=['red', 'orange', 'gray', 'green', 'blue'])
    ax.set_title("Egograma - Perfil dos Estados do Ego")
    ax.set_xlabel("Estados do Ego")
    ax.set_ylabel("Pontuação")
    ax.set_ylim(0, 15)  # 3 questões, max 5 pts cada -> 15
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()

    png_buf = io.BytesIO()
    fig.savefig(png_buf, format="png")
    plt.close(fig)
    png_buf.seek(0)
    return png_buf

def make_table_data(d: dict, header_left="Dimensão", header_right="Pontuação"):
    data = [[header_left, header_right]]
    for k, v in d.items():
        data.append([k, str(v)])
    return data

def build_pdf(egograma_scores, td_scores, td_sit_scores, egograma_png: io.BytesIO) -> bytes:
    """Monta o PDF em memória e retorna os bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    story = []

    # Cabeçalho
    story.append(Paragraph("Relatório Psicométrico", styles["Title"]))
    story.append(Paragraph(datetime.now().strftime("Gerado em %d/%m/%Y %H:%M"), styles["Normal"]))
    story.append(Spacer(1, 0.5*cm))

    # Seção 1 - Egograma
    story.append(Paragraph("1) Egograma", styles["Heading2"]))
    table_ego = Table(make_table_data(egograma_scores))
    table_ego.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
    ]))
    story.append(table_ego)
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Gráfico do Egograma:", styles["Italic"]))
    # Salvar o PNG em arquivo temporário da pipeline do ReportLab
    img_temp = io.BytesIO(egograma_png.getvalue())
    story.append(RLImage(img_temp, width=15*cm, height=8*cm))
    story.append(Spacer(1, 0.5*cm))

    # Seção 2 - Triângulo Dramático (tradicional)
    story.append(Paragraph("2) Triângulo Dramático (tradicional)", styles["Heading2"]))
    table_td = Table(make_table_data(td_scores))
    table_td.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
    ]))
    story.append(table_td)
    story.append(Spacer(1, 0.5*cm))

    # Seção 3 - Triângulo Dramático (situacional)
    story.append(Paragraph("3) Triângulo Dramático (situacional)", styles["Heading2"]))
    table_td2 = Table(make_table_data(td_sit_scores))
    table_td2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
    ]))
    story.append(table_td2)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

# =========================
# Dados dos questionários
# =========================
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

# =========================
# Interface
# =========================
st.title("🧠 Autoavaliação: Egograma & Triângulo Dramático")

st.markdown("Ajuste os controles (1 a 5) para cada afirmação e gere seu relatório em PDF.")

# --- Egograma ---
st.header("Egograma")
pontuacoes_egograma = {}
for estado, questoes in perguntas_egograma.items():
    total = 0
    st.subheader(estado)
    for i, q in enumerate(questoes, start=1):
        total += st.slider(q, 1, 5, 3, key=f"ego_{estado}_{i}")
    pontuacoes_egograma[estado] = total

# --- Triângulo Dramático Tradicional ---
st.header("Triângulo Dramático (tradicional)")
td_pontuacoes = {}
for papel, questoes in td_perguntas.items():
    total = 0
    st.subheader(papel)
    for i, q in enumerate(questoes, start=1):
        total += st.slider(q, 1, 5, 3, key=f"td_{papel}_{i}")
    td_pontuacoes[papel] = total

# --- Triângulo Dramático Situacional ---
st.header("Triângulo Dramático (situacional)")
td_pontuacoes_situacionais = {}
for papel, questoes in td_perguntas_situacionais.items():
    total = 0
    st.subheader(f"{papel} (situacional)")
    for i, q in enumerate(questoes, start=1):
        total += st.slider(q, 1, 5, 3, key=f"td_sit_{papel}_{i}")
    td_pontuacoes_situacionais[papel] = total

# =========================
# Botões de ação
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Ver resultados e gráficos"):
        st.subheader("Resultado do Egograma")
        for estado, valor in pontuacoes_egograma.items():
            st.markdown(f"**{estado}**: {valor} pontos")

        # Gráfico Egograma (1ª análise)
        egograma_png = plot_egograma(pontuacoes_egograma)
        st.image(egograma_png, caption="Egograma - Perfil dos Estados do Ego")

        st.subheader("Resultado do Triângulo Dramático (tradicional)")
        for papel, valor in td_pontuacoes.items():
            st.markdown(f"**{papel}**: {valor} pontos")
            if valor >= 13:
                st.warning(f"Você se identifica fortemente com o papel de **{papel}**.")
            elif valor >= 9:
                st.info(f"Você demonstra algumas características do papel de **{papel}**.")
            else:
                st.success(f"Pouca tendência ao papel de **{papel}**.")

        # Gráfico TD tradicional
        fig2, ax2 = plt.subplots(figsize=(6, 3.5))
        ax2.bar(td_pontuacoes.keys(), td_pontuacoes.values(), color=['purple', 'cyan', 'brown'])
        ax2.set_title("Triângulo Dramático - Papéis Psicológicos")
        ax2.set_xlabel("Papéis")
        ax2.set_ylabel("Pontuação")
        ax2.set_ylim(0, 15)
        ax2.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig2)

        st.subheader("Resultado do Triângulo Dramático (Situacional)")
        for papel, valor in td_pontuacoes_situacionais.items():
            st.markdown(f"**{papel}**: {valor} pontos")
            if valor >= 13:
                st.warning(f"Você frequentemente assume o papel de **{papel}** em situações reais.")
            elif valor >= 9:
                st.info(f"Você apresenta algumas tendências ao papel de **{papel}** em seu comportamento.")
            else:
                st.success(f"Baixa tendência a se posicionar como **{papel}**.")

        # Gráfico TD situacional
        fig3, ax3 = plt.subplots(figsize=(6, 3.5))
        ax3.bar(td_pontuacoes_situacionais.keys(), td_pontuacoes_situacionais.values(),
                color=['#9932CC', '#00CED1', '#A52A2A'])
        ax3.set_title("Triângulo Dramático - Situações Reais")
        ax3.set_xlabel("Papéis")
        ax3.set_ylabel("Pontuação")
        ax3.set_ylim(0, 15)
        ax3.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig3)

with col2:
    if st.button("🧾 Gerar PDF com resultados"):
        # Gera PNG do gráfico do Egograma para inserir no PDF
        egograma_png = plot_egograma(pontuacoes_egograma)
        pdf_bytes = build_pdf(pontuacoes_egograma, td_pontuacoes, td_pontuacoes_situacionais, egograma_png)
        st.success("PDF gerado!")
        st.download_button(
            label="⬇️ Baixar Relatório (PDF)",
            data=pdf_bytes,
            file_name="relatorio_psicometrico.pdf",
            mime="application/pdf",
            use_container_width=True
        )

