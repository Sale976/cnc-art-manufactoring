import streamlit as st
import os
import base64
from github import Github  # Potrebno je dodati PyGithub u requirements.txt

# Inicijalizacija stanja za prijavu admina
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False[cite: 2]

# =========================================================================
# ⚙️ RUČNO PODEŠAVANJE VELIČINE
# =========================================================================
VISINA_SLIKE = "650px"  #

# Fabrička konfiguracija stranice
st.set_page_config(
    page_title="CNC Woodworking Gallery", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)[cite: 2]

# --- MODIFIKOVAN CSS (Čist izgled bez skrivenih dugmića) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');
    .stApp {
        background-image: url("https://www.pixelstalk.net/wp-content/uploads/image11/Wood-desktop-background-QHD-2K-with-a-seamless-wooden-plank-floor-pattern-with-natural-wood-tones.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .stApp > header { background-color: transparent !important; }
    .main .block-container {
        background-color: rgba(15, 10, 5, 0.75); 
        padding: 3rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.9);
        border: 1px solid rgba(139, 69, 19, 0.3);
    }
    .vintage-title {
        font-family: 'Lobster', cursive !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
        font-size: 4.5rem !important;
        color: #e2c591 !important;   
        text-transform: capitalize !important;
        text-shadow: 2px 2px 0px #1a2a3a, 4px 4px 0px #1a2a3a, 6px 6px 0px #121e2a, 8px 8px 15px rgba(0,0,0,0.8) !important;
        padding: 20px !important;
    }
    
    /* HTML link koji obmotava sliku i daje prstić svuda */
    .card-link {
        text-decoration: none !important;
        display: block;
        width: 100%;
        cursor: pointer !important;
    }
    
    /* Izgled drvene kartice */
    .card {
        background: rgba(45, 25, 10, 0.85); 
        border-radius: 12px;
        padding: 16px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 215, 150, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 8px 16px rgba(0,0,0,0.6);
        width: 100%;
    }
    
    .card-link:hover .card {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.9);
        border-color: rgba(255, 215, 150, 0.4);
    }
    
    .card-title {
        color: #e6c280; font-size: 1.4rem; font-weight: 600; margin: 15px 0 5px 0; font-family: 'Georgia', serif; text-align: center; text-shadow: 1px 1px 2px rgba(0,0,0,0.9);
    }
    
    /* Stilovi za normalnu dugmad u admin panelu */
    .sidebar-container div.stButton > button {
        background-color: #8b4513 !important; color: #e6c280 !important; border: 1px solid #cda34f !important; border-radius: 6px !important; width: 100% !important; transition: all 0.2s ease;
    }
    .sidebar-container div.stButton > button:hover { background-color: #cda34f !important; color: #2b2724 !important; }
    
    div[data-elementtype="dialog"] { background-color: rgba(35, 20, 10, 0.98) !important; border: 2px solid #cda34f !important; border-radius: 12px !important; padding: 25px !important; }
</style>
""", unsafe_allow_html=True)[cite: 2]

st.markdown('<h1 class="vintage-title">CNC Woodworking Gallery</h1>', unsafe_allow_html=True)[cite: 2]

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)[cite: 2]

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()[cite: 2]

@st.dialog("Pregled projekta", width="large")
def otvori_modal(staza, ime):
    img_b64 = get_image_base64(staza)
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; text-align: center;">
        <img src="data:image/png;base64,{img_b64}" style="max-width: 100%; height: {VISINA_SLIKE}; object-fit: contain; border-radius: 8px; border: 1px solid rgba(255,215,150,0.2); margin: 0 auto;">
        <h3 style="color: #e6c280; font-family: 'Georgia', serif; text-align: center; margin-top: 20px; width: 100%;">{ime}</h3>
    </div>
    """, unsafe_allow_html=True)[cite: 2]

# =========================================================================
# --- STRANICA ZA ADMINISTRATORA (Bočna traka / Sidebar) ---
# =========================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    st.title("🔐 Admin Panel")
    ADMIN_PASSWORD = "malisa_mali"[cite: 2]

    if not st.session_state.logged_in:
        admin_lozinka = st.text_input("Unesite lozinka za admina:", type="password", key="pwd_input")
        if admin_lozinka == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        elif admin_lozinka != "":
            st.error("Pogrešna lozinka!")[cite: 2]
    else:
        st.success("Uspešno ste prijavljeni!")
        st.markdown("---")
        st.subheader("Dodaj novi projekat")
        
        novi_naziv = st.text_input("Naziv projekta:", key="project_title")
        otpremljen_fajl = st.file_uploader("Izaberite sliku projekta:", type=["png", "jpg", "jpeg", "webp", "gif"], key="project_file")[cite: 2]
        
        if st.button("Sačuvaj i objavi 🚀", key="admin_submit_btn"):
            if novi_naziv and otpremljen_fajl:
                ekstenzija = os.path.splitext(otpremljen_fajl.name)[1]
                siguran_naziv = novi_naziv.strip().replace(" ", "_") + ekstenzija
                putanja_za_cuvanje = os.path.join(IMAGE_DIR, siguran_naziv)[cite: 2]
                
                fajl_bajtovi = otpremljen_fajl.getbuffer()
                
                with open(putanja_za_cuvanje, "wb") as f:
                    f.write(fajl_bajtovi)[cite: 2]
                
                try:
                    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
                    REPO_NAME = st.secrets["GITHUB_REPO"]
                    
                    g = Github(GITHUB_TOKEN)
                    repo = g.get_repo(REPO_NAME)
                    
                    github_putanja = f"images/{siguran_naziv}"
                    
                    repo.create_file(
                        path=github_putanja,
                        message=f"Dodat novi CNC rad: {novi_naziv}",
                        content=bytes(fajl_bajtovi),
                        branch="main"
                    )
                    st.success(f"Projekat '{novi_naziv}' je uspešno dodat i poslat na GitHub!")
                    st.rerun()
                except Exception as e:
                    st.warning(f"Slika je sačuvana samo privremeno! (Nisi podesio st.secrets na Streamlitu. Greška: {e})")
            else:
                st.error("Molimo unesite i naziv i sliku.")[cite: 2]
                
        st.markdown("---")
        if st.button("Izloguj se ❌", key="admin_logout_btn"):
            st.session_state.logged_in = False
            if "project_title" in st.session_state: del st.session_state["project_title"]
            if "project_file" in st.session_state: del st.session_state["project_file"]
            if "pwd_input" in st.session_state: del st.session_state["pwd_input"]
            st.rerun()[cite: 2]
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# --- GLAVNI PRIKAZ GALERIJE (Uhvati klik bez st.button dugmadi) ---
# =========================================================================
images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))][cite: 2]

if not images:
    st.info("Nema pronađenih projekata. Otvorite bočni meni da se prijavite kao admin i dodate prve radove.")[cite: 2]
else:
    # 1. Proveravamo da li je korisnik kliknuo na neku sliku (preko URL parametara)
    url_parametri = st.query_params
    if "izabrana_slika" in url_parametri:
        kliknuta_img = url_parametri["izabrana_slika"]
        # Pronalazimo putanju i naziv za izabranu sliku
        if kliknuta_img in images:
            lepi_naziv = os.path.splitext(kliknuta_img)[0].replace("_", " ")
            pun_put = os.path.join(IMAGE_DIR, kliknuta_img)
            
            # Odmah brišemo parametar iz URL-a da se prozor ne bi stalno otvarao pri osvežavanju
            st.query_params.clear()
            # Otvaramo naš veliki, centrirani modal
            otvori_modal(pun_put, lepi_naziv)

    # 2. Renderovanje galerije u 3 kolone
    cols = st.columns(3)[cite: 2]
    for idx, img_name in enumerate(images):
        col = cols[idx % 3]
        proj_name = os.path.splitext(img_name)[0].replace("_", " ")
        img_path = os.path.join(IMAGE_DIR, img_name)[cite: 2]
        
        with col:
            # Čist HTML link: kada klikneš na sliku, sajt se osvežava sa parametrom ?izabrana_slika=ime.png
            st.markdown(f"""
            <a class="card-link" href="?izabrana_slika={img_name}" target="_self">
                <div class="card">
                    <img src="data:image/png;base64,{get_image_base64(img_path)}" style="width:100%; border-radius:6px; aspect-ratio: 4/3; object-fit: cover; border: 2px solid rgba(255,215,150,0.1);">
                    <div class="card-title">{proj_name}</div>
                </div>
            </a>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)[cite: 2]