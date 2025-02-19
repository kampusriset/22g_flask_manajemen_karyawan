from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Karyawan, User

karyawan_controller = Blueprint('karyawan_controller', __name__)

@karyawan_controller.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('karyawan_controller.login'))
    return render_template('dashboard.html')

@karyawan_controller.route('/karyawan')
def index():
    if 'username' not in session:
        return redirect(url_for('karyawan_controller.login'))
    
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'nama')
    sort_order = request.args.get('sort_order', 'asc')
    
    if search_query:
        karyawan = Karyawan.search_karyawan(search_query)
    else:
        karyawan = Karyawan.get_all_karyawan(page=page, sort_by=sort_by, sort_order=sort_order)

    total_karyawan = Karyawan.count_karyawan()
    total_pages = (total_karyawan // 10) + (1 if total_karyawan % 10 > 0 else 0)

    return render_template('index.html', karyawan=karyawan, page=page, total_pages=total_pages, sort_by=sort_by, sort_order=sort_order)

@karyawan_controller.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('karyawan_controller.login'))
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        alamat = request.form['alamat']
        
        if Karyawan.nama_exists(nama):
            flash('Seorang karyawan dengan nama ini sudah ada.', 'error')
            return render_template('create.html')
        
        new_karyawan = Karyawan(nama, jabatan, alamat)
        Karyawan.create_karyawan(new_karyawan)
        return redirect(url_for('karyawan_controller.index'))
    return render_template('create.html')

@karyawan_controller.route('/update/<int:karyawan_id>', methods=['GET', 'POST'])
def update(karyawan_id):
    if 'username' not in session:
        return redirect(url_for('karyawan_controller.login'))
    karyawan = Karyawan.get_karyawan(karyawan_id)
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        alamat = request.form['alamat']
        updated_karyawan = Karyawan(nama, jabatan, alamat)
        Karyawan.update_karyawan(karyawan_id, updated_karyawan)
        return redirect(url_for('karyawan_controller.index'))
    return render_template('update.html', karyawan=karyawan)

@karyawan_controller.route('/delete/<int:karyawan_id>', methods=['POST'])
def delete(karyawan_id):
    if 'username' not in session:
        return redirect(url_for('karyawan_controller.login'))
    Karyawan.delete_karyawan(karyawan_id)
    return redirect(url_for('karyawan_controller.index'))

@karyawan_controller.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.verify_password(username, password):
            session['username'] = username
            return redirect(url_for('karyawan_controller.dashboard'))
        else:
            return render_template('login.html', error='Login gagal. Periksa username atau password!')
    return render_template('login.html')

@karyawan_controller.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('karyawan_controller.login'))

@karyawan_controller.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create_user(username, password)
        return redirect(url_for('karyawan_controller.login'))
    return render_template('register.html')

@karyawan_controller.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('karyawan_controller.login'))
    if request.method == 'POST':
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if User.verify_password(username, old_password):
            User.update_password(username, new_password)
            flash('Password berhasil diubah', 'success')
            return redirect(url_for('karyawan_controller.dashboard'))
        else:
            flash('Password lama salah', 'error')
    return render_template('change_password.html')
