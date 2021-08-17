### Import libraries 
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
plt.style.use('classic')

### import modules
try:
    from app import engine
except:
    print(""" 'engine', not importable from this file """)



def lineplot_analyse(donnees, abscisse, ordonnee, fichier):
    lineplot = sns.lmplot(x=abscisse, y=ordonnee, data=donnees)
    plt.title("Analyse selon le critère : "+ordonnee, size=15)
    leg_std = mpatches.Patch(color='#c2d1f0',
                              label='Population x 10 Millions')
    leg_mean = mpatches.Patch(color='#3266cd', label='Annee + 2000')
 
    plt.legend(handles=[leg_std, leg_mean],
                loc='lower left',
                bbox_to_anchor=(0., -0.33))
    plt.savefig("app/static/"+fichier)
    # plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    print("lineplot OK")
    return 'done'




def graph_corr(donnees, fichier):
    """
    Creates a correlation matrix among :
    - temperatures
    - life expectancy
    - population
    - unemployment rate

    """
    
    graphique = sns.clustermap(donnees.corr(method ='pearson'))
    graphique.fig.suptitle(
        'Correlation Temperature/Esp.Vie/Population/Chomage', color="Indigo",
        size=20)
    plt.tight_layout()
    plt.savefig("app/static/" +fichier)
    # plt.show()
    plt.clf()
    plt.cla()
    plt.close()
    
    print("graph_corr OK")
    return 'done'

###TESTS
LINE_CHART = False
CORRELATION_CHART = True

if __name__=="__main__":
    from dotenv import load_dotenv
    basedir = os.path.realpath(".env")
    load_dotenv(basedir)
    from sqlalchemy import create_engine
    URL = os.environ.get('URI_POSTGRES')
    engine = create_engine(URL, echo=False)
    
    if LINE_CHART:
        population = pd.read_sql_table("population", engine)
        mask = population['pop_country'] == 'FRANCE'
        population_etudiee = population[mask]
        abscisse = "pop_year"
        ordonnee = "pop_value"
        fichier = "graphiques/population.png"
        lineplot_analyse(population_etudiee, abscisse, ordonnee, fichier)
   
    elif CORRELATION_CHART:
        tous_les_pays = pd.read_sql_table("country", engine)
        correlation = tous_les_pays[[
            "country_pop", "country_life_exp",
            "country_unem_rate","country_temp"]]
 
        fichier = "graphiques/corelation.png"
        graph_corr(correlation, fichier)
        


