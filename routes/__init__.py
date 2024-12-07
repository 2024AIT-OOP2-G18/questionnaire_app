from .user import user_bp
from .product import product_bp
from .order import order_bp
from .student_info import student_info_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  order_bp,
  student_info_bp,
]
