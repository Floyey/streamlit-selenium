from time import sleep
import streamlit as st
import sqlalchemy as db
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


class StraemliSwhow:
    # Requête HTTP
    # url = 'https://howlongtobeat.com/?q='

    def page_config(self, page_title):
        st.set_page_config(
            page_title='HowLongToBeat - ' + page_title,
            page_icon='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMgCer9j5SBcBs7cFbXbX-UIwF9ovoTKNL2-Csp_6eKA&s',
            layout='wide',
        )

    def show_sidebar(self):
        st.sidebar.title('Jérémy Boisnard')
        st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMgCer9j5SBcBs7cFbXbX-UIwF9ovoTKNL2-Csp_6eKA&s')
        st.sidebar.subheader('Description de l\'application')
        st.sidebar.markdown('Cette application permet de collecter des données du site How Long To Beat à l\'aide de Selenium et Scrapy')
        st.sidebar.link_button('Lien vers le site', 'https://howlongtobeat.com/')

    def display_game_info(self, game):
        (
            id,
            title,
            img,
            link,
            duration_main,
            duration_extra,
            duration_complete,
            platform,
            genre,
            developer,
            publisher,
            desc,
        ) = game
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader(title)
            st.write(desc)
            st.link_button('Lien vers le site', link)

        with col2:
            col11, col12, col13 = st.columns(3)
            with col11:
                st.write('**Main Story**')
            with col12:
                st.write('**Main + Sides**')
            with col13:
                st.write('**Completionist**')

            col11, col12, col13 = st.columns(3)
            with col11:
                st.write(duration_main)
            with col12:
                st.write(duration_extra)
            with col13:
                st.write(duration_complete)

            col11, col12 = st.columns(2)
            with col11:
                st.write('\n\n**Plateforme :**\n\n' + platform)
            with col12:
                st.write('\n\n**Genre :**\n\n' + genre)

            col11, col12 = st.columns(2)
            with col11:
                st.write('**Développeur :**\n\n' + developer)
            with col12:
                st.write('**Publieur :**\n\n' + publisher)
        with col3:
            st.image(img)

        return id

    def check_if_exist(self, link):
        database = DataBase('database')
        for i in database.select_table('games'):
            if i[3] == link:
                return i
        return False

    def scrap_data(self, link):
        self.driver.get(link)
        sleep(2)

        try: id = self.driver.current_url.split('/')[-1]
        except: id = 'none'

        try: title = self.driver.find_element(By.CLASS_NAME, 'GameHeader_profile_header__q_PID.shadow_text').text
        except: title = 'none'

        try: img = self.driver.find_element(By.CLASS_NAME, 'GameSideBar_game_image__ozUTt.mobile_hide').find_element(By.TAG_NAME, 'img').get_attribute('src').split('?')[0]
        except: img = 'none'

        try: link = self.driver.current_url
        except: link = 'none'

        time_elements = self.driver.find_element(By.CLASS_NAME, 'GameStats_game_times__KHrRY').find_elements(By.TAG_NAME, 'li')

        try: duration_main = time_elements[0].find_element(By.TAG_NAME, 'h5').text
        except: duration_main = 'none'

        try: duration_extra = time_elements[1].find_element(By.TAG_NAME, 'h5').text
        except: duration_extra = 'none'

        try: duration_complete = time_elements[2].find_element(By.TAG_NAME, 'h5').text
        except: duration_complete = 'none'

        try: self.driver.find_element(By.ID, 'profile_summary_more').click()
        except: pass

        try: desc = self.driver.find_elements(By.CLASS_NAME, 'GameSummary_profile_info__HZFQu')[0].text
        except: desc = 'none'

        try: platform = self.driver.find_elements(By.CLASS_NAME, 'GameSummary_profile_info__HZFQu')[2].text.split('\n')[1]
        except: platform = 'none'

        try: genre = self.driver.find_elements(By.CLASS_NAME, 'GameSummary_profile_info__HZFQu')[3].text.split('\n')[1]
        except: genre = 'none'

        try: developer = self.driver.find_elements(By.CLASS_NAME, 'GameSummary_profile_info__HZFQu')[4].text.split('\n')[1]
        except: developer = 'none'

        try: publisher = self.driver.find_elements(By.CLASS_NAME, 'GameSummary_profile_info__HZFQu')[5].text.split('\n')[1]
        except: publisher = 'none'

        data = [
            id,
            title,
            img,
            link,
            duration_main,
            duration_extra,
            duration_complete,
            platform,
            genre,
            developer,
            publisher,
            desc
        ]

        self.database = DataBase('database')
        self.database.add_row('games', title=title, img=img, link=link, duration_main=duration_main, duration_extra=duration_extra, duration_complete=duration_complete, platform=platform, genre=genre, developer=developer, publisher=publisher, desc=desc)

        self.display_game_info(data)

    def show_games(self, game_name = ''):
        self.database = DataBase('database')
        data_games = {}

        if game_name == '':
            for game in self.database.select_table('games'):
                st.markdown('<hr>', unsafe_allow_html=True)
                id = self.display_game_info(game)
                data_games[id] = game
        else:
            self.driver = Chrome()
            self.driver.get(f"https://howlongtobeat.com/?q={game_name}")
            sleep(2)
            self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

            cards = self.driver.find_elements(By.CLASS_NAME, 'GameCard_inside_blur__cP8_l')
            links = []
            for card in cards:
                link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                try:
                    links.index(link)
                    continue
                except:
                    links.append(link)
                    pass

            for link in links:
                is_exist = self.check_if_exist(link)
                if is_exist == False:
                    self.scrap_data(link)
                else:
                    self.display_game_info(is_exist)

            self.driver.close()

        df = pd.DataFrame(data_games).T

        csv = convert_df(df)

        st.sidebar.download_button(
            label='Télécharger les données',
            data=csv,
            file_name='games.csv',
            mime='text/csv'
        )

@st.cache_resource
def convert_df(df):
    return df.to_csv().encode('utf-8')


class DataBase:
    def __init__(self, name_database='database'):
        self.name = name_database
        self.url = f'sqlite:///{name_database}.db'
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.engine.table_names()

    def create_table(self, name_table, **kwargs):
        colums = [db.Column(k, v, primary_key=True) if 'id_' in k else db.Column(k, v) for k, v in kwargs.items()]
        db.Table(name_table, self.metadata, *colums)
        try: self.metadata.create_all(self.engine)
        except: pass

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        if return_keys: table.columns.keys()
        else: return table

    def add_row(self, name_table, **kwarrgs):
        table = self.read_table(name_table)
        stmt = db.insert(table).values(kwarrgs)
        self.connection.execute(stmt)

    def select_table(self, name_table):
        name_table = self.read_table(name_table)
        stm = db.select([name_table])
        return self.connection.execute(stm).fetchall()

streamlit = StraemliSwhow()
