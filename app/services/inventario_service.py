from decimal import Decimal

from app.constants import MOVIMIENTO_INGRESO, MOVIMIENTO_SALIDA
from app.extensions import db
from app.models.movimiento import MovimientoInventario


class InventarioError(Exception):
    pass


def calcular_subtotal(cantidad: int, precio) -> Decimal:
    return Decimal(str(cantidad)) * Decimal(str(precio))


def registrar_movimiento(
    producto,
    tipo: str,
    cantidad: int,
    stock_anterior: int,
    stock_nuevo: int,
    referencia_tipo: str,
    referencia_id: int,
    usuario_id: int,
    observacion: str | None = None,
):
    movimiento = MovimientoInventario(
        producto_id=producto.id,
        tipo=tipo,
        cantidad=cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=stock_nuevo,
        referencia_tipo=referencia_tipo,
        referencia_id=referencia_id,
        usuario_id=usuario_id,
        observacion=observacion,
    )
    db.session.add(movimiento)


def aplicar_ingreso_detalle(detalle, usuario_id: int):
    producto = detalle.producto
    stock_anterior = producto.stock
    producto.stock = stock_anterior + detalle.cantidad
    producto.precio_compra = detalle.precio_compra

    registrar_movimiento(
        producto=producto,
        tipo=MOVIMIENTO_INGRESO,
        cantidad=detalle.cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=producto.stock,
        referencia_tipo="ingreso",
        referencia_id=detalle.ingreso_id,
        usuario_id=usuario_id,
        observacion=f"Ingreso #{detalle.ingreso_id}",
    )


def aplicar_salida_detalle(detalle, usuario_id: int):
    producto = detalle.producto
    if producto.stock < detalle.cantidad:
        raise InventarioError(
            f"Stock insuficiente para '{producto.nombre}'. "
            f"Disponible: {producto.stock}, solicitado: {detalle.cantidad}."
        )

    stock_anterior = producto.stock
    producto.stock = stock_anterior - detalle.cantidad

    registrar_movimiento(
        producto=producto,
        tipo=MOVIMIENTO_SALIDA,
        cantidad=detalle.cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=producto.stock,
        referencia_tipo="salida",
        referencia_id=detalle.salida_id,
        usuario_id=usuario_id,
        observacion=f"Venta #{detalle.salida_id}",
    )


def revertir_ingreso_detalle(detalle, usuario_id: int):
    producto = detalle.producto
    if producto.stock < detalle.cantidad:
        raise InventarioError(
            f"No se puede revertir el ingreso: stock insuficiente en '{producto.nombre}'."
        )

    stock_anterior = producto.stock
    producto.stock = stock_anterior - detalle.cantidad

    registrar_movimiento(
        producto=producto,
        tipo=MOVIMIENTO_SALIDA,
        cantidad=detalle.cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=producto.stock,
        referencia_tipo="ingreso_reverso",
        referencia_id=detalle.ingreso_id,
        usuario_id=usuario_id,
        observacion=f"Reversión ingreso #{detalle.ingreso_id}",
    )


def revertir_salida_detalle(detalle, usuario_id: int):
    producto = detalle.producto
    stock_anterior = producto.stock
    producto.stock = stock_anterior + detalle.cantidad

    registrar_movimiento(
        producto=producto,
        tipo=MOVIMIENTO_INGRESO,
        cantidad=detalle.cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=producto.stock,
        referencia_tipo="salida_reverso",
        referencia_id=detalle.salida_id,
        usuario_id=usuario_id,
        observacion=f"Reversión venta #{detalle.salida_id}",
    )


def recalcular_total_salida(salida):
    total = sum((detalle.subtotal for detalle in salida.detalles), Decimal("0"))
    salida.total = total
