import streamlit as st
import os
import base64

# Inicijalizacija stanja za prijavu admina
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Fabrička konfiguracija stranice (zatvoren sidebar pri prvoj poseti)
st.set_page_config(
    page_title="CNC Woodworking Gallery", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# =========================================================================
# --- CUSTOM CSS STILIZACIJA (Pozadina, Kartice, Fontovi i Popup) ---
# =========================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

    /* Pozadina celog sajta - tekstura drveta */
    .stApp {
        background-image: url("https://www.pixelstalk.net/wp-content/uploads/image11/Wood-desktop-background-QHD-2K-with-a-seamless-wooden-plank-floor-pattern-with-natural-wood-tones.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    
    .stApp > header {
        background-color: transparent !important;
    }
    
    /* Tamni poluprovidni štit preko pozadine radi bolje čitljivosti */
    .main .block-container {
        background-color: rgba(15, 10, 5, 0.75); 
        padding: 3rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.9);
        border: 1px solid rgba(139, 69, 19, 0.3);
    }
    
    /* Prelepi Retro Vintage Naslov */
    .vintage-title {
        font-family: 'Lobster', cursive !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
        font-size: 4.5rem !important;
        color: #e2c591 !important;   
        text-transform: capitalize !important;
        text-shadow: 
            2px 2px 0px #1a2a3a, 
            4px 4px 0px #1a2a3a, 
            6px 6px 0px #121e2a,
            8px 8px 15px rgba(0,0,0,0.8) !important;
        padding: 20px !important;
    }
    
    /* Elegantne rustične kartice za projekte */
    .card {
        background: rgba(45, 25, 10, 0.85); 
        border-radius: 12px;
        padding: 16px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 215, 150, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 8px 16px rgba(0,0,0,0.6);
        margin-bottom: 5px;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.9);
        border-color: rgba(255, 215, 150, 0.4);
    }
    
    .card-title {
        color: #e6c280;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 15px 0 5px 0;
        font-family: 'Georgia', serif;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.9);
    }

    /* Stilizacija svih dugmadi u aplikaciji */
    div.stButton > button {
        background-color: #8b4513 !important;
        color: #e6c280 !important;
        border: 1px solid #cda34f !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #cda34f !important;
        color: #2b2724 !important;
    }

    /* Stilizacija iskačućeg prozora (st.dialog) - uklanjanje sivih ivica */
    div[data-elementtype="dialog"] {
        background-color: rgba(35, 20, 10, 0.98) !important;
        border: 2px solid #cda34f !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    div[data-elementtype="dialog"] h3 {
        color: #e6c280 !important;
        font-family: 'Georgia', serif;
    }
</style>
""", unsafe_allow_html=True)

# Glavni naslov aplikacije
st.markdown('<h1 class="vintage-title">CNC Woodworking Gallery</h1>', unsafe_allow_html=True)

# Folder u kome se skladište slike
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Funkcija za otvaranje umerenog i čistog popup prozora (width="small")
@st.dialog("Pregled projekta", width="small")
def otvori_modal(staza, ime):
    st.image(staza, width="stretch")
    st.markdown(f"<h3 style='text-align:center; margin-top:15px;'>{ime}</h3>", unsafe_allow_html=True)


# =========================================================================
# --- STRANICA ZA ADMINISTRATORA (Bočna traka / Sidebar) ---
# =========================================================================
with st.sidebar:
    st.title("🔐 Admin Panel")
    ADMIN_PASSWORD = "malisa_mali"  # Ovde menjaš lozinku za pristup

    # Provera da li je admin prijavljen
    if not st.session_state.logged_in:
        admin_lozinka = st.text_input("Unesite lozinku za admina:", type="password", key="pwd_input")
        if admin_lozinka == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        elif admin_lozinka != "":
            st.error("Pogrešna lozinka!")

    else:
        st.success("Uspešno ste prijavljeni!")
        st.markdown("---")
        st.subheader("Dodaj novi projekat")
        
        novi_naziv = st.text_input("Naziv projekta:", key="project_title")
        otpremljen_fajl = st.file_uploader("Izaberite sliku projekta:", type=["png", "jpg", "jpeg", "webp", "gif"], key="project_file")
        
        if st.button("Sačuvaj i objavi 🚀"):
            if novi_naziv and otpremljen_fajl:
                ekstenzija = os.path.splitext(otpremljen_fajl.name)[1]
                # Menjamo razmake u donje crte radi bezbednosti fajlova na disku
                siguran_naziv = novi_naziv.strip().replace(" ", "_") + ekstenzija
                putanja_za_cuvanje = os.path.join(IMAGE_DIR, siguran_naziv)
                
                with open(putanja_za_cuvanje, "wb") as f:
                    f.write(otpremljen_fajl.getbuffer())
                    
                st.success(f"Projekat '{novi_naziv}' je uspešno dodat!")
                st.rerun()
            else:
                st.error("Molimo unesite i naziv i sliku.")
                
        st.markdown("---")
        
        # Dugme za odjavu i pražnjenje admin panela
        if st.button("Izloguj se ❌"):
            st.session_state.logged_in = False
            
            # Čišćenje stanja forme iz memorije aplikacije
            if "project_title" in st.session_state: del st.session_state["project_title"]
            if "project_file" in st.session_state: del st.session_state["project_file"]
            if "pwd_input" in st.session_state: del st.session_state["pwd_input"]
            
            st.rerun()


# =========================================================================
# --- GLAVNI PRIKAZ GALERIJE (Za sve posetioce) ---
# =========================================================================
images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))]

if not images:
    st.info("Nema pronađenih projekata. Otvorite bočni meni da se prijavite kao admin i dodate prve radove.")
else:
    # Generisanje mreže od 3 kolone
    cols = st.columns(3)
    for idx, img_name in enumerate(images):
        col = cols[idx % 3]
        
        # Sređivanje imena fajla za lep prikaz na kartici
        proj_name = os.path.splitext(img_name)[0].replace("_", " ")
        img_path = os.path.join(IMAGE_DIR, img_name)
        
        with col:
            # Prikaz kartice
            st.markdown(f"""
            <div class="card">
                <img src="data:image/png;base64,{get_image_base64(img_path)}" style="width:100%; border-radius:6px; aspect-ratio: 4/3; object-fit: cover; border: 2px solid rgba(255,215,150,0.1);">
                <div class="card-title">{proj_name}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Dugme za iskakanje slike u umerenoj veličini
            if st.button("Povećaj sliku 🔍", key=f"btn_{idx}"):
                otvori_modal(img_path, proj_name)
            
            st.markdown("<br>", unsafe_allow_html=True)
