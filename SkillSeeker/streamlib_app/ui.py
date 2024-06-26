import streamlit as st
import requests
from app.db import get_db
from app.models import Planner


placeholder = st.empty()
if 'menu' not in locals(): 
    menu = 'login'
if menu == 'login':
        page = st.sidebar.selectbox("Choose a page", ["Register", "Login", "Request", 'History', 'Global History'], key='login_page_select')
        if page == "Register":
            st.header("Register")
            rut = st.text_input("RUT", key='register_rut')
            name = st.text_input("Name", key='register_name')
            password = st.text_input("Password", type="password", key='register_password')
            if st.button("Register", key='register_button'):
                response = requests.post("http://localhost:8000/register", json={"rut": rut, "name": name, "password": password})
                if response.status_code == 200:

                    st.success("Registered successfully")
                else:
                    st.error("An error occurred")

        elif page == "Login":
            st.header("Login")
            rut = st.text_input("RUT", key='login_rut')
            password = st.text_input("Password", type="password", key='login_password')
            if st.button("Login", key='login_button'):
                response = requests.post("http://localhost:8000/login", data={"username": rut, "password": password})
                if response.status_code == 200:
                    st.success("Logged in successfully")
                    menu = 'request'
                    db = get_db()
                    cur = db.cursor()
                    cur.execute("SELECT * FROM Planner WHERE id = ?", (response.json(),))
                    user = cur.fetchall()[0]
                    db
                    planner = Planner(user[2], user[1], user[0])
                    st.session_state['planner'] = planner
                    placeholder.empty()
                    
                else:
                    st.error("An error occurred")

        elif page == 'Request':
            if 'planner' not in st.session_state:
                st.error("You must login first")
            else:
                with placeholder.container():
                    st.header("Request")
                    query = st.text_input("Query", key='request_query')
                    if st.button("Request", key='request_button'):

                        planner = st.session_state['planner']
                        st.session_state['planner'] = planner
                        st.success('Please wait')
                        response = requests.post("http://localhost:8000/request", json={"description": query, "planner_id": planner.getId(), "request_id": 0})
                        planner.generateRequest(query, planner.getId(), int(response.json()))
    
                        if response.status_code == 200:
                            st.success("Request sent successfully")
                        else:
                            st.error("An error occurred")
        elif page == 'History':
            if 'planner' not in st.session_state:
                st.error("You must login first")
            else:
                st.header("History")
                # Obtener el ID del planner
                planner_id = st.session_state['planner'].getId()
    
                # Hacer una consulta a la base de datos para obtener las búsquedas y talleristas asociados a un planner
                response = requests.get(f"http://localhost:8000/requesthistory?planner_id={planner_id}")
                if response.status_code == 200:
                    requests_data = response.json()
                    st.write('Requests:')
                    for request in requests_data:
                        button1 = st.button(request[1], key = request[0])
                        if st.session_state.get('button') != True:
                            st.session_state['button'] = button1
                        if st.session_state['button'] == True:
                            response = requests.get(f"http://localhost:8000/workshopleaderhistory?request_id={request[0]}")
                            if response.status_code == 200:
                                workshop_leaders = response.json()
                                for workshop_leader in workshop_leaders:
                                        st.markdown(f"**Nombre:** {workshop_leader[1]}")
                                        st.markdown(f"**Descripción:** {workshop_leader[2]}")
                                        if workshop_leader[3] != '':
                                            st.markdown(f"**Teléfono:** {workshop_leader[3]}")
                                        if workshop_leader[4] != '':
                                            st.markdown(f"**Email:** {workshop_leader[4]}")
                                        if workshop_leader[5] != '':
                                            st.markdown(f"**Redes sociales:** {workshop_leader[5]}")
                                        if workshop_leader[8] == 1:
                                            st.markdown(f"**Favorito:** Contacto validado")
                                        elif workshop_leader[8] == 0:
                                            st.markdown(f"**Contacto:** Contacto no validado")
                                        workshop_leader_id = "id"+ str(workshop_leader[0])
                                        if  workshop_leader[7] == 0:
                                            print(workshop_leader[0])
                                            if st.button('Set Favorite', workshop_leader_id):
                                                response = requests.put("http://localhost:8000/favorite/"+ str(workshop_leader[0]))
                                                print(response.json())
                                                if response.status_code == 200:
                                                    st.success("Workshop leader favorited successfully")
                                                else:
                                                    st.error("An error occurred while favoriting the workshop leader")
                                            
                                        if  workshop_leader[7] == 1:
                                            if st.button('Unset Favorite', workshop_leader_id):
                                                response = requests.put("http://localhost:8000/unfavorite/" + str(workshop_leader[0]))
                                                if response.status_code == 200:
                                                    st.success("Workshop leader unfavorited successfully")
                                                else:
                                                    st.error("An error occurred while unfavoriting the workshop leader")
                                            
                                        if workshop_leader[8] == 0:
                                            if st.button('Valid contact', workshop_leader_id+'_contact'):
                                                response = requests.put("http://localhost:8000/contacted/" + str(workshop_leader[0]))
                                                if response.status_code == 200:
                                                    st.success("Workshop leader contacted successfully")
                                                else:
                                                    st.error("An error occurred while contacting the workshop leader")
                                            st.markdown("---")
                                        else:
                                            st.markdown("---")
                            else:
                                st.error("An error occurred while getting the workshop leaders")
                else:
                    st.error("An error occurred while getting the requests")
        elif page == 'Global History':
            if 'planner' not in st.session_state:
                st.error("You must login first")
            else:
                st.header("Global History")
                # Obtener el ID del planner
                planner_id = st.session_state['planner'].getId()

                response = requests.get(f"http://localhost:8000/workshopleaderhistoryglobal")
                if response.status_code == 200:
                    
                    workshop_leaders = response.json()
                    print(workshop_leaders)
                    for workshop_leader in workshop_leaders:
                        st.markdown(f"**Nombre:** {workshop_leader[1]}")
                        st.markdown(f"**Descripción:** {workshop_leader[2]}")
                        if workshop_leader[3] != '':
                            st.markdown(f"**Teléfono:** {workshop_leader[3]}")
                        if workshop_leader[4] != '':
                            st.markdown(f"**Email:** {workshop_leader[4]}")
                        if workshop_leader[5] != '':
                            st.markdown(f"**Redes sociales:** {workshop_leader[5]}")
                        st.markdown("---")
                else:
                     st.error("An error occurred while getting the workshop leaders")
                
