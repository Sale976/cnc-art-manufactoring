import streamlit as st
import os
import base64

# Inicijalizacija stanja za prijavu admina
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================================================
# ⚙️ RUČNO PODEŠAVANJE VELIČINE VELIKE SLIKE NA KLIK
# =========================================================================
VISINA_SLIKE = "80vh"  # Koristimo 80% visine ekrana kako bi uvek bila savršena

# Fabrička konfiguracija stranice
st.set_page_config(
    page_title="CNC Woodworking Gallery", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- MODIFIKOVAN CSS ---
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
        cursor: pointer !important;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.9);
        border-color: rgba(255, 215, 150, 0.4);
    }
    
    .card-title {
        color: #e6c280; font-size: 1.4rem; font-weight: 600; margin: 15px 0 5px 0; font-family: 'Georgia', serif; text-align: center; text-shadow: 1px 1px 2px rgba(0,0,0,0.9);
    }
    
    /* --- LIGHTBOX SISTEM --- */
    .lightbox {
        display: none;
        position: fixed;
        z-index: 99999;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background: rgba(15, 10, 5, 0.6); 
        backdrop-filter: blur(5px);
    }

    .lightbox:target {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .lightbox-content {
        position: relative;
        display: inline-block;
        max-width: 90%;
        max-height: 75vh;
    }

    .lightbox-content img {
        display: block;
        max-width: 100%;
        max-height: 75vh;
        border-radius: 8px;
        border: 2px solid #cda34f;
        box-shadow: 0 0 35px rgba(0,0,0,0.9);
    }
    
    .lightbox-close {
        position: absolute;
        top: -15px;
        right: -15px;
        background: #2d190a;
        color: #e6c280;
        width: 40px;
        height: 40px;
        line-height: 36px;
        text-align: center;
        border-radius: 50%;
        border: 2px solid #cda34f;
        font-size: 28px;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.7);
        transition: color 0.2s, transform 0.2s, background-color 0.2s;
        z-index: 100000;
    }
    
    .lightbox-close:hover {
        color: #fff;
        background-color: #8b4513;
        transform: scale(1.1);
    }
    
    .lightbox-caption {
        color: #e6c280;
        font-family: 'Georgia', serif;
        font-size: 1.8rem;
        margin-top: 20px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.9);
        text-align: center;
    }

    /* Stilovi za normalnu dugmad u admin panelu */
    .sidebar-container div.stButton > button {
        background-color: #8b4513 !important; color: #e6c280 !important; border: 1px solid #cda34f !important; border-radius: 6px !important; width: 100% !important; transition: all 0.2s ease;
    }
    .sidebar-container div.stButton > button:hover { background-color: #cda34f !important; color: #2b2724 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="vintage-title">CNC Woodworking Gallery</h1>', unsafe_allow_html=True)

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Čitamo sve dostupne slike iz foldera
images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))]

# =========================================================================
# --- STRANICA ZA ADMINISTRATORA (Bočna traka / Sidebar) ---
# =========================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    st.title("🔐 Admin Panel")
    ADMIN_PASSWORD = "malisa_mali"

    if not st.session_state.logged_in:
        admin_lozinka = st.text_input("Unesite lozinka za admina:", type="password", key="pwd_input")
        if admin_lozinka == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        elif admin_lozinka != "":
            st.error("Pogrešna lozinka!")
    else:
        st.success("Uspešno ste prijavljeni!")
        st.markdown("---")
        
        # --- SEKCIJA 1: DODAVANJE PROJEKATA ---
        st.subheader("Dodaj novi projekat")
        novi_naziv = st.text_input("Naziv projekta:", key="project_title")
        otpremljen_fajl = st.file_uploader("Izaberite sliku projekta:", type=["png", "jpg", "jpeg", "webp", "gif"], key="project_file")
        
        if st.button("Sačuvaj i objavi 🚀", key="admin_submit_btn"):
            if novi_naziv and otpremljen_fajl:
                ekstenzija = os.path.splitext(otpremljen_fajl.name)[1]
                siguran_naziv = novi_naziv.strip().replace(" ", "_") + ekstenzija
                putanja_za_cuvanje = os.path.join(IMAGE_DIR, siguran_naziv)
                
                fajl_bajtovi = otpremljen_fajl.getbuffer()
                
                with open(putanja_za_cuvanje, "wb") as f:
                    f.write(fajl_bajtovi)
                
                try:
                    from github import Github
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
                st.error("Molimo unesite i naziv i sliku.")
                
        st.markdown("---")
        
        # --- NOVA SEKCIJA 2: BRISANJE PROJEKATA (Samo ako ima slika u galeriji) ---
        st.subheader("🗑️ Obriši projekat")
        if images:
            # Kreiramo pregledan rečnik gde je ključ "Lep Naziv.png", a vrednost pravo ime fajla
            opcije_za_brisanje = {f.replace("_", " "): f for f in images}
            izabrani_lepi_naziv = st.selectbox("Izaberite rad za brisanje:", options=list(opcije_za_brisanje.keys()))
            fajl_za_brisanje = opcije_za_brisanje[izabrani_lepi_naziv]
            
            if st.button("Izbriši trajno 🗑️", key="admin_delete_btn"):
                # 1. Brisanje sa lokalnog servera (Streamlit Cloud privremene memorije)
                lokalna_putanja = os.path.join(IMAGE_DIR, fajl_za_brisanje)
                if os.path.exists(lokalna_putanja):
                    os.remove(lokalna_putanja)
                
                # 2. Brisanje direktno sa GitHub-a da se slika ne vrati
                try:
                    from github import Github
                    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
                    REPO_NAME = st.secrets["GITHUB_REPO"]
                    
                    g = Github(GITHUB_TOKEN)
                    repo = g.get_repo(REPO_NAME)
                    
                    github_putanja = f"images/{fajl_za_brisanje}"
                    
                    # Moramo prvo povući fajl sa GitHub-a da bismo dobili njegov jedinstveni "sha" kod za brisanje
                    contents = repo.get_contents(github_putanja, ref="main")
                    
                    repo.delete_file(
                        path=github_putanja,
                        message=f"Obrisan CNC rad: {izabrani_lepi_naziv}",
                        sha=contents.sha,
                        branch="main"
                    )
                    st.success(f"Uspesno obrisan rad '{izabrani_lepi_naziv}' sa sajta i GitHub-a!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Greška pri brisanju sa GitHub-a. Proveri st.secrets. Greška: {e}")
        else:
            st.info("Trenutno nema slika za brisanje.")
            
        st.markdown("---")
        if st.button("Izloguj se ❌", key="admin_logout_btn"):
            st.session_state.logged_in = False
            if "project_title" in st.session_state: del st.session_state["project_title"]
            if "project_file" in st.session_state: del st.session_state["project_file"]
            if "pwd_input" in st.session_state: del st.session_state["pwd_input"]
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# --- GLAVNI PRIKAZ GALERIJE ---
# =========================================================================
if not images:
    st.info("Nema pronađenih projekata. Otvorite bočni meni da se prijavite kao admin i dodate prve radove.")
else:
    cols = st.columns(3)
    for idx, img_name in enumerate(images):
        col = cols[idx % 3]
        proj_name = os.path.splitext(img_name)[0].replace("_", " ")
        img_path = os.path.join(IMAGE_DIR, img_name)
        img_b64 = get_image_base64(img_path)
        
        with col:
            st.markdown(f"""
            <a href="#img_{idx}" style="text-decoration: none; color: inherit;">
                <div class="card">
                    <img src="data:image/png;base64,{img_b64}" style="width:100%; border-radius:6px; aspect-ratio: 4/3; object-fit: cover; border: 2px solid rgba(255,215,150,0.1);">
                    <div class="card-title">{proj_name}</div>
                </div>
            </a>

            <div id="img_{idx}" class="lightbox">
                <div class="lightbox-content">
                    <a href="#" class="lightbox-close">&times;</a>
                    <img src="data:image/png;base64,{img_b64}">
                </div>
                <div class="lightbox-caption">{proj_name}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)