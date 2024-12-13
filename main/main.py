import os
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import MySQLdb as mdb
import mysql.connector  # Thay vì import MySQLdb as mdb
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt  
from datetime import datetime
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6.QtCore import QDate
import mysql.connector

# Đường dẫn đến các tệp UI
ui_path = "D:/python web/main"

# Đăng Nhập
class Login_w(QMainWindow):
    
    def __init__(self):
        super(Login_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'dangnhap.ui'), self)
        self.btndangnhap.clicked.connect(self.login)
        self.txtmk.setEchoMode(QLineEdit.EchoMode.Password)
        self.showPasswordRadioButton.toggled.connect(self.toggle_password_visibility)

class Login_w(QMainWindow):

    def __init__(self):
        super(Login_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'dangnhap.ui'), self)
        self.btndangnhap.clicked.connect(self.login)
        self.txtmk.setEchoMode(QLineEdit.EchoMode.Password)
        self.showPasswordRadioButton.toggled.connect(self.toggle_password_visibility)

    def login(self):
        tk = self.txttentk.text()  
        mk = self.txtmk.text()     
        if not tk or not mk:
            QMessageBox.warning(self, "Thông Báo", "Vui lòng điền đầy đủ thông tin đăng nhập")
            return
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM quanly WHERE username = %s AND password = %s", (tk, mk))
            kt_quanly = query.fetchone()
            if kt_quanly:
                QMessageBox.information(self, "Login", "Đăng Nhập Thành Công (Admin)")
                widget.setCurrentIndex(2)  
            else:
                query.execute("SELECT * FROM user WHERE tentk = %s AND matkhau = %s", (tk, mk))
                kt_user = query.fetchone()
                if kt_user:
                    QMessageBox.information(self, "Login", "Đăng Nhập Thành Công (Nhân Viên)")
                    widget.setCurrentIndex(3)
                    self.parent().setFixedSize(950, 600)
                else:
                    QMessageBox.information(self, "Login", "Đăng Nhập Thất Bại")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            if 'db' in locals() and db:
                db.close()


    def showEvent(self, event):
        self.parent().setFixedSize(450, 360)
        super().showEvent(event)
    
    def toggle_password_visibility(self, checked):
        if checked:
            self.txtmk.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.txtmk.setEchoMode(QLineEdit.EchoMode.Password)
            
# Đăng Kí
class dangki_w(QMainWindow):
    
    def __init__(self):
        super(dangki_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'dangki.ui'), self)
        self.btnxacnhan.clicked.connect(self.reg)
        self.btnhuy.clicked.connect(self.huy)
        
    def huy(self):
        widget.setCurrentIndex(0) 
        self.parent().setFixedSize(450, 400)
        
    def reg(self):
        ht = self.txthoten.toPlainText()
        gt = self.txtgioitinh.toPlainText()
        ns = self.datengaysinh.date().toString("yyyy-MM-dd")
        sdt = self.txtsdt.toPlainText()
        diachi = self.txtdiachi.toPlainText()
        email = self.txtemail.toPlainText()
        tentk = self.txttentaikhoan.toPlainText()
        matkhau = self.txtmatkhau.toPlainText()
        if not all([ht, gt, ns, sdt, diachi, email, matkhau]):
            QMessageBox.warning(self, "Thông Báo", "Vui lòng điền đầy đủ thông tin")
            return
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM user WHERE Email = %s AND matkhau = %s", (email, matkhau))
            kt = query.fetchone()
            if kt:
                QMessageBox.warning(self, "Thông Báo", "Tài khoản đã tồn tại")
            else:
                query.execute("INSERT INTO user (Hoten, gioitinh, ngaysinh, sdt, diachi, Email, tentk, matkhau) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                          (ht, gt, ns, sdt, diachi, email, tentk, matkhau))
                db.commit()
                QMessageBox.information(self, "Thông Báo", "Đăng ký thành công")
                widget.setCurrentIndex(0)
        except mysql.connector.Error as e:  # Thay đổi mdb.Error thành mysql.connector.Error
            QMessageBox.critical(self, "Database Error", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            if 'db' in locals() and db:
                db.close()
            
    def showEvent(self, event):
        self.parent().setFixedSize(450, 500)  
        super().showEvent(event)

# Trang Chủ Quản Lý
class trangchu_w(QMainWindow):
    
    def __init__(self):
        super(trangchu_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'trangchu.ui'), self)
        self.btndangxuat.clicked.connect(self.dangxuat)
        self.btnaddsp.clicked.connect(self.themsp)
        self.btnhoadon.clicked.connect(self.hoadon)
        self.btnthongke.clicked.connect(self.thongke)
        self.btnttkhachhang.clicked.connect(self.ttkh)
        self.btndangki.clicked.connect(self.reg_from)
        self.btnbanhang.clicked.connect(self.banhang)
        self.tbqlshop.itemSelectionChanged.connect(self.on_item_selection_changed5)
        
    def themsp(self):
        widget.setCurrentIndex(7)  
        
    def hoadon(self):
        widget.setCurrentIndex(8)  
        
    def thongke(self):
        widget.setCurrentIndex(9)  
        
    def ttkh(self):
        widget.setCurrentIndex(10)  
        
    def dangxuat(self):
        widget.setCurrentIndex(0) 
        
    def reg_from(self):
        widget.setCurrentIndex(1)
        
    def banhang(self):
        widget.setCurrentIndex(3)
        
    def load_sanpham_quanly(self):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM sanpham")
            results = query.fetchall()
            self.tbqlshop.setRowCount(0)  
            for row_number, row_data in enumerate(results):
                self.tbqlshop.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    if column_number in [0, 2, 3]: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    elif column_number in [1]:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    else: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.tbqlshop.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
        self.tbqlshop.setColumnWidth(0, 150)
        self.tbqlshop.setColumnWidth(1, 300)
        self.tbqlshop.setColumnWidth(2, 100)
        self.tbqlshop.setColumnWidth(3, 100)
        self.tbqlshop.setColumnWidth(4, 100)
        
    def on_item_selection_changed5(self):
        selected_items = self.tbqlshop.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.delete_row5(row)

    def delete_row5(self, row):
        item = self.tbqlshop.item(row, 0)
        if item is not None:  
            id = item.text() 
            reply = QMessageBox.question(self, "Thông Báo", "Bạn muốn xóa hàng này?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    db = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='',
                        database='python',
                        use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
                    )
                    query = db.cursor()
                    query.execute("DELETE FROM sanpham WHERE id = %s", (id,))
                    db.commit()
                    QMessageBox.information(self, "Thông Báo", "Xóa sản phẩm thành công")
                    self.load_sanpham_quanly()  
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi xóa sản phẩm: {e}")
                finally:
                    db.close()
        
    def showEvent(self, event):
        self.parent().setFixedSize(850, 630)
        super().showEvent(event)
        self.load_sanpham_quanly()

# Thêm Sản Phẩm Quản Lý
class themsanpham_w(QMainWindow):
    
    def __init__(self):
        super(themsanpham_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'themsanpham.ui'), self)
        self.btnthemsp.clicked.connect(self.themsp)
        self.btnhuysp.clicked.connect(self.huysp)
        
    def themsp(self):
        id = self.txtmasp.toPlainText()
        tensp = self.txttensp.toPlainText()
        soluong = self.txtsoluong.toPlainText()
        size = self.txtsize.toPlainText()
        gia = self.txtgiatien.toPlainText()
        if not all([id, tensp, soluong, size, gia]):
            QMessageBox.warning(self, "Thông Báo", "Vui lòng điền đầy đủ thông tin")
            return
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            gia = float(gia)
            query.execute("INSERT INTO sanpham (id, tensp, soluong, size, gia) VALUES (%s, %s, %s, %s, %s)",
                          (id, tensp, soluong, size, gia))
            db.commit()
            QMessageBox.information(self, "Thông Báo", "Thêm sản phẩm thành công")
            self.clear_inputs()
            widget.setCurrentIndex(2)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
            
    def clear_inputs(self):
        self.txtmasp.setPlainText("")
        self.txttensp.setPlainText("")
        self.txtsoluong.setPlainText("")
        self.txtsize.setPlainText("")
        self.txtgiatien.setPlainText("")
        
    def huysp(self):
        widget.setCurrentIndex(2)
        self.parent().setFixedSize(850, 630)
        
    def showEvent(self, event):
        self.parent().setFixedSize(500, 450) 
        super().showEvent(event)
        
# Hóa Đơn Quản Lý
class hoadonn_w(QMainWindow):
    
    def __init__(self):
        super(hoadonn_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'hoadonql.ui'), self)
        self.btnthoathd.clicked.connect(self.thoathd)
        self.tbhoadon2.cellClicked.connect(self.on_cell_clicked)
        self.tbhoadon2.itemSelectionChanged.connect(self.on_item_selection_changed2)

    def thoathd(self):
        widget.setCurrentIndex(2) 
        self.parent().setFixedSize(850, 630)
        
    def load_hoadon_data(self):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM hoadon")
            results = query.fetchall()
            self.tbhoadon2.setRowCount(0)  
            for row_number, row_data in enumerate(results):
                self.tbhoadon2.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable) 
                    if column_number in [0, 1, 3, 4]: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    elif column_number in [5]:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    else: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.tbhoadon2.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
            
    def on_cell_clicked(self, row, column):
        if column == self.tbhoadon2.columnCount() - 1: 
            details_item = self.tbhoadon2.item(row, column)
            if details_item:
                details = details_item.text()
                QMessageBox.information(self, "Chi Tiết Hóa Đơn", details)
        else:
            self.delete_row2(row)
    
    def on_item_selection_changed2(self):
        selected_items = self.tbhoadon2.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.delete_row2(row)

    def delete_row2(self, row):
        item = self.tbhoadon2.item(row, 0)
        if item is not None:  
            id = item.text() 
            reply = QMessageBox.question(self, "Thông Báo", "Bạn muốn xóa hàng này?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    db = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='',
                        database='python',
                        use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
                    )
                    query = db.cursor()
                    query.execute("DELETE FROM hoadon WHERE id = %s", (id,))
                    db.commit()
                    QMessageBox.information(self, "Thông báo", "Xóa hóa đơn thành công")
                    self.load_hoadon_data()  
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi xóa hóa đơn: {e}")
                finally:
                    db.close()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một hàng để xóa")

    def showEvent(self, event):
        self.parent().setFixedSize(750, 400)  
        super().showEvent(event)
        self.load_hoadon_data()

# Thống Kê Quản Lý
class thongke_w(QMainWindow):
    
    def __init__(self):
        super(thongke_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'thongke.ui'), self)
        self.btnqlai.clicked.connect(self.quaylai)
        self.btnThongKeNgay.clicked.connect(self.thong_ke_ngay)
        self.btnThongKeThang.clicked.connect(self.thong_ke_thang)
        self.btnThongKeNam.clicked.connect(self.thong_ke_nam)

    def quaylai(self):
        widget.setCurrentIndex(2)  
        self.parent().setFixedSize(850, 630)

    def thong_ke_ngay(self):
        ngay = str(self.spinBoxNgay.value())
        thang = str(self.spinBoxThang.value())
        nam = str(self.spinBoxNam.value())
        ngay_thang = f"{nam}-{thang}-{ngay}"
        self.thong_ke("ngay", ngay_thang)

    def thong_ke_thang(self):
        thang = str(self.spinBoxThang.value()).zfill(2)
        self.thong_ke("thang", thang)
    
    def thong_ke_nam(self):
        nam = str(self.spinBoxNam.value())
        self.thong_ke("nam", nam)
        
    def thong_ke(self, theo, gia_tri):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            if theo == "ngay":
                query.execute("SELECT COUNT(id), SUM(tongtien) FROM hoadon WHERE DATE(ngaytao) = %s", (gia_tri,))
            elif theo == "thang":
                query.execute("SELECT COUNT(id), SUM(tongtien) FROM hoadon WHERE MONTH(ngaytao) = %s", (gia_tri,))
            elif theo == "nam":
                query.execute("SELECT COUNT(id), SUM(tongtien) FROM hoadon WHERE YEAR(ngaytao) = %s", (gia_tri,))
            result = query.fetchone()
            tong_don_hang = result[0]
            tong_thu_nhap = result[1]
            self.lblTongDonHang.setText(f"Tổng đơn hàng: {tong_don_hang}")
            self.lblTongThuNhap.setText(f"Tổng thu nhập: {tong_thu_nhap}")
        except mysql.connector.Error as e:
            if theo == "ngay":
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi thực hiện thống kê theo ngày: {e}")
            elif theo == "thang":
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi thực hiện thống kê theo tháng: {e}")
            elif theo == "nam":
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi thực hiện thống kê theo năm: {e}")
        finally:
            db.close()
            
    def showEvent(self, event):
        self.parent().setFixedSize(680, 480) 
        super().showEvent(event)
        
# Thông Tin Khách Hàng Quản Lý
class ttkh_w(QMainWindow):
    
    def __init__(self):
        super(ttkh_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'ttkhquanly.ui'), self)
        self.btnokkhql.clicked.connect(self.okkhql)
        self.tbkhql.itemSelectionChanged.connect(self.on_item_selection_changed1)
        
    def okkhql(self):
        widget.setCurrentIndex(2)  
        self.parent().setFixedSize(850, 630)
        
    def load_khachhang_data2(self):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM khachhang")
            results = query.fetchall()
            self.tbkhql.setRowCount(0)  
            for row_number, row_data in enumerate(results):
                self.tbkhql.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable) 
                    if column_number in [0, 2, 3, 4, 5]: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    else: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.tbkhql.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
        self.tbkhql.setColumnWidth(0, 100)
        self.tbkhql.setColumnWidth(1, 280)
        self.tbkhql.setColumnWidth(2, 110)
        self.tbkhql.setColumnWidth(3, 100)
        self.tbkhql.setColumnWidth(4, 100)
        self.tbkhql.setColumnWidth(5, 100)
        self.tbkhql.setColumnWidth(6, 180)

    def on_item_selection_changed1(self):
        selected_items = self.tbkhql.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.delete_row(row)

    def delete_row(self, row):
        item = self.tbkhql.item(row, 0)
        if item is not None:  
            id = item.text() 
            reply = QMessageBox.question(self, "Thông Báo", "Bạn muốn xóa hàng này?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    db = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='',
                        database='python',
                        use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
                    )
                    query = db.cursor()
                    query.execute("DELETE FROM khachhang WHERE id = %s", (id,))
                    db.commit()
                    QMessageBox.information(self, "Thông báo", "Xóa khách hàng thành công")
                    self.load_khachhang_data2()  
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi xóa khách hàng: {e}")
                finally:
                    db.close()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một hàng để xóa")
        
    def showEvent(self, event):
        self.parent().setFixedSize(1050, 550)  
        super().showEvent(event) 
        self.load_khachhang_data2()       

# Trang Chủ Nhân Viên 
class trangchunv_w(QMainWindow):
    
    def __init__(self):
        super(trangchunv_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'tcNhanVien.ui'), self)
        self.btndangxuatnv.clicked.connect(self.dangxuatnv)
        self.btnaddkh.clicked.connect(self.addkh)
        self.btntaohd.clicked.connect(self.taohd)
        self.btnxemttkh.clicked.connect(self.xemttkh)
        self.btntim1.clicked.connect(self.timkiem)

    def timkiem(self):
        keyword = self.txttimkiem.toPlainText().strip()
        if keyword:
            try:
                db = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='python',
                    use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
                )
                query = db.cursor()
                query.execute("SELECT * FROM sanpham WHERE id LIKE %s OR tensp LIKE %s OR gia LIKE %s OR soluong LIKE %s", 
                              (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
                results = query.fetchall()
                self.tbspnv.setRowCount(0)
                for row_number, row_data in enumerate(results):
                    self.tbspnv.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data))
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        if column_number in [0, 2, 3]: 
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        elif column_number in [4]:
                            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                        else: 
                            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                        self.tbspnv.setItem(row_number, column_number, item)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
            finally:
                db.close()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm")

    def taohd(self):
        widget.setCurrentIndex(5)  
            
    def addkh(self):
        widget.setCurrentIndex(4) 
        
    def xemttkh(self):
        widget.setCurrentIndex(6) 
        
    def dangxuatnv(self):
        widget.setCurrentIndex(0) 
        self.parent().setFixedSize(450, 400)
    
    def load_sanpham_data(self):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM sanpham")
            results = query.fetchall()
            self.tbspnv.setRowCount(0)  
            for row_number, row_data in enumerate(results):
                self.tbspnv.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    if column_number in [0, 2, 3]: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    elif column_number in [4]:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    else: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.tbspnv.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
        self.tbspnv.setColumnWidth(0, 100)
        self.tbspnv.setColumnWidth(1, 280)
        self.tbspnv.setColumnWidth(2, 100)
        self.tbspnv.setColumnWidth(3, 100)
        self.tbspnv.setColumnWidth(4, 100)
    
    def showEvent(self, event):
        self.parent().setFixedSize(950, 600)  
        self.load_sanpham_data()
       
# Thêm Khách Hàng Nhân viên
class addkhachhang_w(QMainWindow):
    
    def __init__(self):
        super(addkhachhang_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'addkhachhang.ui'), self)
        self.btnluukh.clicked.connect(self.luukh)
        self.btnhuykh.clicked.connect(self.huykh)

    def luukh(self):
        id = self.txtmakh.toPlainText()
        tenkh = self.txttenkh.toPlainText()
        ngaysinh = self.datenskh.date().toString("yyyy-MM-dd")
        gioitinh = self.txtgtkh.toPlainText()
        sdt = self.txtsdtkh.toPlainText()
        diachi = self.txtdckh.toPlainText()
        email = self.txtemailkh.toPlainText()
        if not all([id, tenkh, ngaysinh, gioitinh, sdt, diachi, email]):
            QMessageBox.warning(self, "Thông Báo", "Vui lòng điền đầy đủ thông tin")
            return
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("INSERT INTO `khachhang`(`id`, `tenkh`, `ngaysinh`, `gioitinh`, `sdt`, `diachi`, `email`)  VALUES (%s, %s, %s, %s, %s, %s, %s)",
                          (id, tenkh, ngaysinh, gioitinh, sdt, diachi, email))
            db.commit()
            QMessageBox.information(self, "Thông Báo", "Thêm khách hàng thành công")
            self.clear_inputs()
            widget.setCurrentIndex(3)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
            
    def clear_inputs(self):
        self.txtmakh.setPlainText("")
        self.txttenkh.setPlainText("")
        self.datenskh.setDate(QDate.currentDate())
        self.txtgtkh.setPlainText("")
        self.txtsdtkh.setPlainText("")
        self.txtdckh.setPlainText("")
        self.txtemailkh.setPlainText("")
        
    def huykh(self):
        widget.setCurrentIndex(3) 
        self.parent().setFixedSize(950, 600)

    def showEvent(self, event):
        self.parent().setFixedSize(650, 600)  
        super().showEvent(event)

# Tạo Hóa Đơn Nhân Viên
class taohoadon_w(QMainWindow):
    
    def __init__(self):
        super(taohoadon_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'taohoadon.ui'), self)
        self.btnhuysptt.clicked.connect(self.huytt)
        self.btnthanhtoan.clicked.connect(self.thanhtoan)
        self.btnokk.clicked.connect(self.okk)
        self.btnokk2.clicked.connect(self.okk2)
        self.tbtksptt.itemSelectionChanged.connect(self.on_item_selection_changed)

    def okk(self):
        keyword = self.txttimsptt.toPlainText().strip()
        if keyword:
            self.search_sanpham(keyword)
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm")

    def search_sanpham(self, keyword):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM sanpham WHERE id LIKE %s OR tensp LIKE %s OR gia LIKE %s OR soluong LIKE %s", 
                          (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            results = query.fetchall()
            self.tbtksptt.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.tbtksptt.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    if column_number in [0, 2, 3]: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    elif column_number in [4]:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    else: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.tbtksptt.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
        
    def okk2(self):
        keyword = self.txttimsptt2.toPlainText().strip()
        if keyword:
            self.search_khachhang(keyword)
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm")

    def search_khachhang(self, keyword):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM khachhang WHERE id LIKE %s OR tenkh LIKE %s", (f'%{keyword}%', f'%{keyword}%'))
            result = query.fetchone() 
            self.tbkhtt.setRowCount(1)
            if result:
                for column_number, data in enumerate(result):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    if column_number in [0, 2, 3, 4, 5]: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    else: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.tbkhtt.setItem(0, column_number, item)
            else:
                QMessageBox.warning(self, "Thông báo", "Không tìm thấy thông tin khách hàng")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()
        self.tbsptt.setColumnWidth(0, 100)
        self.tbsptt.setColumnWidth(1, 280)
        self.tbsptt.setColumnWidth(2, 100)
        self.tbsptt.setColumnWidth(3, 100)
        self.tbsptt.setColumnWidth(4, 100)

    def on_item_selection_changed(self):
        selected_items = self.tbtksptt.selectedItems()
        if selected_items:
            reply = QMessageBox.question(self, "Xác nhận", "Bạn muốn chọn sản phẩm này?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                for item in selected_items:
                    row = item.row()
                    self.tbsptt.setRowCount(self.tbsptt.rowCount() + 1)
                    for column in range(self.tbtksptt.columnCount()):
                        item = self.tbtksptt.item(row, column)
                        if item is not None:
                            self.tbsptt.setItem(self.tbsptt.rowCount() - 1, column, QTableWidgetItem(item.text()))
                for item in selected_items:
                    row = item.row()
                    self.tbtksptt.removeRow(row)
                self.tbsptt.setColumnWidth(0, 100)
                self.tbsptt.setColumnWidth(1, 280)
                self.tbsptt.setColumnWidth(2, 100)
                self.tbsptt.setColumnWidth(3, 100)
                self.tbsptt.setColumnWidth(4, 100)

    def huytt(self):
        widget.setCurrentIndex(3)  
        self.parent().setFixedSize(950, 600)

    def thanhtoan(self):
        total_price = self.calculate_total_price()
        id = self.tbkhtt.item(0, 0).text()  
        tenkh = self.tbkhtt.item(0, 1).text() 
        sdt = self.tbkhtt.item(0, 4).text()  
        ngay_tao_hd = datetime.now().strftime("%Y-%m-%d")

        hoadon = f"""HÓA ĐƠN
            Mã khách hàng: {id}
            Tên khách hàng: {tenkh}
            Số điện thoại: {sdt}
            Ngày tạo hóa đơn: {ngay_tao_hd}
            Sản phẩm:
            """
        for row in range(self.tbsptt.rowCount()):
            id_sanpham = self.tbsptt.item(row, 0).text()
            tensp = self.tbsptt.item(row, 1).text()
            gia = self.tbsptt.item(row, 4).text()
            hoadon += f"\n{id_sanpham} - Tên SP: {tensp}, Giá: {gia}\n"
        hoadon += f"\nTổng số tiền: {total_price}\n"
        QMessageBox.information(self, "Hóa đơn", hoadon)
        file_name, ok = QInputDialog.getText(self, "Nhập tên hóa đơn", "Nhập tên cho hóa đơn:")
        if ok:
            self.create_invoice_pdf(id, tenkh, sdt, hoadon, f"{file_name}.pdf")
            QMessageBox.information(self, "Thành công", f"Hóa đơn đã được lưu với tên {file_name}.pdf")
            try:
                db = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='python',
                    use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
                )               
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO hoadon (makhachhang, tenkhachhang, sodienthoai, ngaytao, tongtien, chitiet) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, tenkh, sdt, ngay_tao_hd, total_price, hoadon)
                )
                for row in range(self.tbsptt.rowCount()):
                    id_sanpham = self.tbsptt.item(row, 0).text()
                    query = "UPDATE sanpham SET soluong = soluong - 1 WHERE id = %s"
                    cursor.execute(query, (id_sanpham,))
                db.commit()
                self.tbkhtt.setRowCount(0)  
                self.tbsptt.setRowCount(0) 
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
            finally:
                db.close()


    def calculate_total_price(self):
        total_price = 0
        for row in range(self.tbsptt.rowCount()):
            gia = float(self.tbsptt.item(row, 4).text())
            total_price += gia 
        return total_price

    def create_invoice_pdf(self, customer_id, customer_name, customer_phone, invoice_content, file_name):
        font_path = "D:/python web/main/DejaVuSans.ttf"
        pdfmetrics.registerFont(TTFont('DejaVu', font_path))
        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter
        c.setFont("DejaVu", 12)
        c.drawString(50, height - 50, "-------HÓA ĐƠN-------")
        c.drawString(50, height - 100, f"Tên khách hàng: {customer_name}")
        c.drawString(50, height - 120, f"Số điện thoại: {customer_phone}")
        lines = invoice_content.split('\n')
        y_position = height - 150
        for line in lines:
            c.drawString(50, y_position, line)
            y_position -= 20
        c.save()

    def showEvent(self, event):
        self.parent().setFixedSize(950, 700)
        super().showEvent(event)

# Thông Tin Khách Hàng Nhân Viên
class xemttkh_w(QMainWindow):
    
    def __init__(self):
        super(xemttkh_w, self).__init__()
        uic.loadUi(os.path.join(ui_path, 'thongtinkhachhang.ui'), self)
        self.btnokkh.clicked.connect(self.okkh)
        self.tbkh1.itemSelectionChanged.connect(self.on_item_selection_changed)

    def okkh(self):
        widget.setCurrentIndex(3)  
        self.parent().setFixedSize(950, 600)

    def showEvent(self, event):
        self.parent().setFixedSize(780, 550) 
        self.load_khachhang_data()
     
    def load_khachhang_data(self):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='python',
                use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
            )
            query = db.cursor()
            query.execute("SELECT * FROM khachhang")
            results = query.fetchall()
            self.tbkh1.setRowCount(0)  
            for row_number, row_data in enumerate(results):
                self.tbkh1.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  
                    if column_number in [0, 2, 3, 4, 5]: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    else: 
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.tbkh1.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        finally:
            db.close()

    def on_item_selection_changed(self):
        selected_items = self.tbkh1.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.delete_row(row)

    def delete_row(self, row):
        item = self.tbkh1.item(row, 0)
        if item is not None:  
            id = item.text() 
            reply = QMessageBox.question(self, "Thông Báo", "Bạn muốn xóa hàng này?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    db = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='',
                        database='python',
                        use_pure=True  # Sử dụng mysql-connector-python hỗ trợ use_pure
                    )
                    query = db.cursor()
                    query.execute("DELETE FROM khachhang WHERE id = %s", (id,))
                    db.commit()
                    QMessageBox.information(self, "Thông báo", "Xóa khách hàng thành công")
                    self.load_khachhang_data()  
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi xóa khách hàng: {e}")
                finally:
                    db.close()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một hàng để xóa")

# Xử Lý Thứ Tự Và Hiển Thị 
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
# Thứ Tự
dangnhap_f = Login_w()   
dangki_f = dangki_w()
trangchu_f = trangchu_w()
trangchunv_f = trangchunv_w()
addkhachhang_f = addkhachhang_w()
taohoadon_f = taohoadon_w()
xemttkh_f = xemttkh_w()
themsanpham_f = themsanpham_w()
hoadonn_f = hoadonn_w()
thongke_f = thongke_w()
ttkh_f = ttkh_w()

widget.addWidget(dangnhap_f)
widget.addWidget(dangki_f)
widget.addWidget(trangchu_f)
widget.addWidget(trangchunv_f)
widget.addWidget(addkhachhang_f)
widget.addWidget(taohoadon_f)
widget.addWidget(xemttkh_f)
widget.addWidget(themsanpham_f)
widget.addWidget(hoadonn_f)
widget.addWidget(thongke_f)
widget.addWidget(ttkh_f)

# Trang Hiển Thị Đầu Tiên
widget.setCurrentIndex(0)
widget.show()

try:
    sys.exit(app.exec())
except Exception as e:
    print(f"Lỗi khi chạy ứng dụng: {e}")
