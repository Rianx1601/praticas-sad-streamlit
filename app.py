
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard - Student Dataset", page_icon=":books:")

st.sidebar.title("Configurações de Exibição")

gsheets_show_id = st.sidebar.radio("Selecione o Dataset", ("Matemática", "Português"))

st.sidebar.subheader("Selecione o que deseja exibir")
show_dataset = st.sidebar.checkbox("Dados do Dataset")
show_dataset_description = st.sidebar.checkbox("Descrição do Dataset")

graph1_type = st.sidebar.selectbox("Gráfico 1: Selecione o tipo de gráfico", ("Barra", "Pizza", "Dispersão", "Histograma", "Boxplot"))

gsheets_math_id = "1392993996"
gsheets_portuguese_id = "0"

show_id = gsheets_math_id if gsheets_show_id == "Matemática" else gsheets_portuguese_id

gsheets_url = 'https://docs.google.com/spreadsheets/d/1pfqNNPJrB1QFcqUm5evvDeijycnuPFDztInZvl3nOyU/edit#gid=' + show_id
@st.cache_data(ttl=120)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

data = load_data(gsheets_url)

st.title("Análise de Dados do Dataset de Estudantes")

if show_dataset_description:
    st.subheader("Descrição do Dataset")

    st.markdown("""
| Column    | Description                                                                                        |
|-----------|----------------------------------------------------------------------------------------------------|
| school    | Student's school (binary: 'GP' - Gabriel Pereira or 'MS' - Mousinho da Silveira)                   |
| sex       | Student's sex (binary: 'F' - female or 'M' - male)                                               |
| age       | Student's age (numeric: from 15 to 22)                                                            |
| address   | Student's home address type (binary: 'U' - urban or 'R' - rural)                                  |
| famsize   | Family size (binary: 'LE3' - less or equal to 3 or 'GT3' - greater than 3)                         |
| Pstatus   | Parent's cohabitation status (binary: 'T' - living together or 'A' - apart)                       |
| Medu      | Mother's education (numeric: 0 - none, 1 - primary education (4th grade), 2 - 5th to 9th grade, 3 - secondary education or 4 - higher education) |
| Fedu      | Father's education (numeric: 0 - none, 1 - primary education (4th grade), 2 - 5th to 9th grade, 3 - secondary education or 4 - higher education) |
| Mjob      | Mother's job (nominal: 'teacher', 'health' care related, civil 'services' (e.g. administrative or police), 'at_home' or 'other') |
| Fjob      | Father's job (nominal: 'teacher', 'health' care related, civil 'services' (e.g. administrative or police), 'at_home' or 'other') |
| reason    | Reason to choose this school (nominal: close to 'home', school 'reputation', 'course' preference or 'other') |
| guardian  | Student's guardian (nominal: 'mother', 'father' or 'other')                                        |
| traveltime| Home to school travel time (numeric: 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour) |
| studytime | Weekly study time (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)   |
| failures  | Number of past class failures (numeric: n if 1<=n<3, else 4)                                       |
| schoolsup | Extra educational support (binary: yes or no)                                                      |
| famsup    | Family educational support (binary: yes or no)                                                     |
| paid      | Extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)               |
| activities| Extra-curricular activities (binary: yes or no)                                                    |
| nursery   | Attended nursery school (binary: yes or no)                                                        |
| higher    | Wants to take higher education (binary: yes or no)                                                 |
| internet  | Internet access at home (binary: yes or no)                                                        |
| romantic  | With a romantic relationship (binary: yes or no)                                                   |
| famrel    | Quality of family relationships (numeric: from 1 - very bad to 5 - excellent)                       |
| freetime  | Free time after school (numeric: from 1 - very low to 5 - very high)                               |
| goout     | Going out with friends (numeric: from 1 - very low to 5 - very high)                               |
| Dalc      | Workday alcohol consumption (numeric: from 1 - very low to 5 - very high)                          |
| Walc      | Weekend alcohol consumption (numeric: from 1 - very low to 5 - very high)                          |
| health    | Current health status (numeric: from 1 - very bad to 5 - very good)                                |
| absences  | Number of school absences (numeric: from 0 to 93)                                                  |
""")            

if show_dataset:
    st.subheader("Conjunto de Dados")
    st.dataframe(data)

st.subheader("Média de Idade dos Estudantes por Escola")
school_mean_age = data.groupby('school')['age'].mean()
fig, ax = plt.subplots()
sns.barplot(x=school_mean_age.index, y=school_mean_age.values)
ax.set_xlabel('Escola')
ax.set_ylabel('Media da idade dos Estudantes')
st.pyplot(fig)


st.subheader("Moda do endereço dos alunos na escola MS")
school_moda_address = data[data.school == 'MS']['address'].mode()
match school_moda_address.values[0]:
    case 'U':
        st.write("Urbano")
    case 'R':
        st.write("Rural")
    case _:
        st.write("Não informado")


st.subheader("Qual é a médiana do tempo de viagem dos alunos que estudam na escolaGP")
school_median_traveltime = data[data.school == 'GP']['traveltime'].median()

match school_median_traveltime:
    case 1.0:
        st.write("Menos de 15 minutos")
    case 2.0:
        st.write("Entre 15 e 30 minutos")
    case 3.0:
        st.write("Entre 30 minutos e 1 hora")
    case 4.0:
        st.write("Mais de 1 hora")
    case _:
        st.write("Não informado")



st.subheader("Qual é o desvio padrão da idade dos alunos que têm apoio educacional extra na escola MS")
school_std_age = data[(data.school == 'MS') & (data.schoolsup == 'yes')]['age'].std()
st.write(school_std_age)

st.subheader("Qual é a média do tempo semanal de estudo dos alunos cujos pais estão separados na escola GP")
school_mean_studytime = data[(data.school == 'GP') & (data.Pstatus == 'A')]['studytime'].mean()
match school_mean_studytime:
    case 1.0:
        st.write("Menos de 2 horas")
    case 2.0:
        st.write("Entre 2 e 5 horas")
    case 3.0:
        st.write("Entre 5 e 10 horas")
    case 4.0:
        st.write("Mais de 10 horas")
    case _:
        st.write("Não informado")


st.subheader("Qual é a moda do motivo pelo qual os alunos escolheram a escola MS?")
school_moda_reason = data[data.school == 'MS']['reason'].mode()
match school_moda_reason.values[0]:
    case 'home':
        st.write("Proximidade da casa")
    case 'reputation':
        st.write("Reputação da escola")
    case 'course':
        st.write("Preferência pelo curso")
    case 'other':
        st.write("Outros")
    case _:
        st.write("Não informado")
   
st.subheader("Qual é a mediana do número de faltas dos alunos que frequentam a escola GP?")
school_median_absences = data[data.school == 'GP']['absences'].median()
st.write(school_median_absences)

st.subheader("Qual é o desvio padrão do nível de saúde dos alunos que frequentam atividades extracurriculares na escola MS?")
school_std_health = data[(data.school == 'MS') & (data.activities == 'yes')]['health'].std()
match school_std_health:
    case 1.0:
        st.write("Muito ruim")
    case 2.0:
        st.write("Ruim")
    case 3.0:
        st.write("Regular")
    case 4.0:
        st.write("Bom")
    case 5.0:
        st.write("Muito bom")
    case _:
        st.write("Não informado")

   
st.subheader("Quantos alunos já cumpriram as horas extracurriculares?")
school_count_activities = data[data.activities == 'yes']['activities'].count()
st.write(school_count_activities)
  
st.subheader("Qual é a moda do consumo de álcool dos alunos da escola MS durante a semana de trabalho?")
school_moda_workday_alcohol = data[data.school == 'MS']['Dalc'].mode()
match school_moda_workday_alcohol.values[0]:
    case 1.0:
        st.write("Muito baixo")
    case 2.0:
        st.write("Baixo")
    case 3.0:
        st.write("Regular")
    case 4.0:
        st.write("Alto")
    case 5.0:
        st.write("Muito alto")
    case _:
        st.write("Não informado")
        
