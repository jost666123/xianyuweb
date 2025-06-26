from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user

from .models import db, Product
from .app import AdminUser # Import AdminUser from app.py
from .forms import ProductForm # Import ProductForm

# This function will be called in app.py to register routes.
def register_routes(app):

    @app.route('/')
    def index():
        try:
            products = Product.query.order_by(Product.created_at.desc()).all()
        except Exception as e:
            print(f"Error fetching products: {e}")
            products = []
            flash("无法加载产品数据，请确保数据库已正确初始化。", "warning")
        return render_template('index.html', products=products, title="主页")

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))

        # Using a simple form for now, will replace with Flask-WTF if time permits for login form
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            admin_config_username = current_app.config['ADMIN_USERNAME']
            user = AdminUser.get_by_username(username)

            if user and user.username == admin_config_username and user.check_password(password):
                login_user(user)
                flash('登录成功!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('admin_dashboard'))
            else:
                flash('用户名或密码错误。', 'danger')

        return render_template('admin_login.html', title="管理员登录")

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        flash('您已成功注销。', 'info')
        return redirect(url_for('admin_login'))

    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        try:
            products = Product.query.order_by(Product.updated_at.desc()).all()
        except Exception as e:
            print(f"Error fetching products for admin dashboard: {e}")
            products = []
            flash("无法加载产品列表。", "danger")
        return render_template('admin_dashboard.html', title="管理后台", username=current_user.username, products=products)

    @app.route('/stats')
    def stats():
        # Actual stats calculation will be added in a later step
        total_products = 0
        total_profit_sum = 0
        total_exposure_sum = 0
        total_sales_sum = 0
        try:
            total_products = Product.query.count()
            # Ensure profit is not None before summing
            profits = [p.profit for p in Product.query.all() if p.profit is not None]
            total_profit_sum = sum(profits) if profits else 0

            exposures = [p.exposure for p in Product.query.all() if p.exposure is not None]
            total_exposure_sum = sum(exposures) if exposures else 0

            sales = [p.sales_count for p in Product.query.all() if p.sales_count is not None]
            total_sales_sum = sum(sales) if sales else 0

        except Exception as e:
            print(f"Error calculating stats: {e}")
            flash("无法加载统计数据。", "warning")

        return render_template('stats.html', title="数据统计",
                               total_products=total_products,
                               total_profit_sum=total_profit_sum,
                               total_exposure_sum=total_exposure_sum,
                               total_sales_sum=total_sales_sum)

    @app.route('/admin/products/add', methods=['GET', 'POST'])
    @login_required
    def add_product():
        form = ProductForm()
        if form.validate_on_submit():
            new_product = Product(
                title=form.title.data,
                description=form.description.data,
                image_url=form.image_url.data,
                purchase_url=form.purchase_url.data,
                purchase_price=form.purchase_price.data,
                selling_url=form.selling_url.data,
                selling_price=form.selling_price.data,
                exposure=form.exposure.data,
                sales_count=form.sales_count.data
            )
            new_product.calculate_profit() # Calculate and set profit
            db.session.add(new_product)
            try:
                db.session.commit()
                flash('新产品已成功添加!', 'success')
                return redirect(url_for('admin_dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'添加产品时发生错误: {e}', 'danger')
        return render_template('product_form.html', title="添加新产品", form=form, form_action=url_for('add_product'))

    @app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
    @login_required
    def edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        form = ProductForm(obj=product) # Pre-populate form with product data

        if form.validate_on_submit():
            product.title = form.title.data
            product.description = form.description.data
            product.image_url = form.image_url.data
            product.purchase_url = form.purchase_url.data
            product.purchase_price = form.purchase_price.data
            product.selling_url = form.selling_url.data
            product.selling_price = form.selling_price.data
            product.exposure = form.exposure.data
            product.sales_count = form.sales_count.data
            product.calculate_profit() # Recalculate profit

            db.session.add(product) # or db.session.merge(product) if you prefer
            try:
                db.session.commit()
                flash('产品信息已更新!', 'success')
                return redirect(url_for('admin_dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'更新产品时发生错误: {e}', 'danger')

        return render_template('product_form.html', title="编辑产品", form=form, product=product, form_action=url_for('edit_product', product_id=product.id))

    @app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
    @login_required
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        try:
            db.session.delete(product)
            db.session.commit()
            flash('产品已删除!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'删除产品时发生错误: {e}', 'danger')
        return redirect(url_for('admin_dashboard'))
