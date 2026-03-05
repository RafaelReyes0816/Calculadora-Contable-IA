# Fallback de seguridad en caso de que se borre el excel
data = {
    'descripcion': [
        'Compra de papel bond para oficina', 'Compra de libros contables', 'Compra de material de escritorio',
        'Compra de bolígrafos y carpetas', 'Compra de grapas y engargolados', 'Compra de sobres y etiquetas',
        'Adquisición de computadoras laptop', 'Adquisición de impresora', 'Compra de celular para gerente',
        'Compra de monitor pantalla', 'Compra de teclado y mouse', 'Compra de disco duro externo',
        'Pago de servicios de internet', 'Pago de agua y luz', 'Pago de teléfono', 'Pago de energía eléctrica',
        'Pago de servicio de agua potable', 'Compra de útiles de limpieza', 'Compra de jabón y desinfectante',
        'Compra de escobas y trapeadores', 'Compra de papel higiénico', 'Adquisición de mobiliario de oficina',
        'Compra de escritorio', 'Compra de sillas', 'Compra de archiveros metálicos', 'Compra de estantes',
        'Compra de mercadería para reventa', 'Compra de productos para venta', 'Compra de inventario',
        'Compra de repuestos para vehículos', 'Pago de gasolina vehículos', 'Compra de aceite para motor',
        'Mantenimiento de flota vehicular', 'Servicio de asesoría legal', 'Pago de honorarios abogado',
        'Servicio de consultoría contable', 'Pago de auditoría externa', 'Compra de alimentos para personal',
        'Compra de carne para asado', 'Compra de almuerzos para empleados', 'Compra de refrigerios para reunión',
        'Pago de viáticos alimentación', 'Compra de tornillos y herramientas', 'Compra de martillo y destornilladores',
        'Compra de equipo de seguridad', 'Pago de alquiler de local', 'Pago de renta de oficina', 'Alquiler de bodega',
        'Venta de productos terminados', 'Venta de mercadería al contado', 'Prestación de servicios profesionales',
        'Venta de maquinaria usada', 'Venta de servicios', 'Facturación de servicios', 'Pago de gasolina vehículos',
        'Compra de diesel para flota', 'Carga de combustible', 'Pago de seguros', 'Gastos de representación',
        'Comisiones bancarias', 'Pago de licencias de software',
        'Compra de televisor LED', 'Compra de pantalla smart TV', 'Adquisición de televisor 4K',
        'Compra de proyector', 'Adquisición de cañonera',
        'Compra de refrigerador', 'Adquisición de nevera',
        'Compra de microondas', 'Compra de licuadora',
        'Servicio de hosting web', 'Pago de dominio internet',
        'Compra de cámara fotográfica', 'Adquisición de webcam',
        'Pago de pasajes', 'Compra de boletos aéreos',
        'Compra de impresora 3D', 'Adquisición de plotter',
        # Nuevos: Hogar / Muebles
        'Compra de cama matrimonial', 'Adquisición de sofá para sala',
        'Compra de comedor de madera', 'Adquisición de ropero',
        # Nuevos: Equipos de Computación
        'Compra de servidor rack', 'Adquisición de tarjeta gráfica',
        'Compra de memoria RAM', 'Compra de procesador intel',
        'Compra de placa base', 'Adquisición de tablet iPad',
        'Compra de router inalámbrico', 'Compra de switch de red',
        # Nuevos: Comidas y Víveres
        'Compra de mercado para la semana', 'Adquisición de víveres',
        'Compra de verduras y frutas', 'Pago de cuenta en restaurante',
        'Compra de comida rápida', 'Compra de snacks y bebidas',
        'Compra de café y azúcar', 'Compra de desayuno ejecutivo',
        # Nuevos: Productos para el hogar / Limpieza
        'Compra de detergente para ropa', 'Adquisición de lavandina y cloro',
        'Compra de desodorante ambiental', 'Compra de bolsas de basura',
        'Compra de cera para pisos', 'Compra de esponjas y lavavajillas',
        # Nuevos: Electrodomésticos
        'Compra de lavadora de ropa', 'Adquisición de secadora',
        'Compra de cocina a gas', 'Compra de estufa eléctrica',
        'Compra de horno eléctrico', 'Compra de aire acondicionado',
        # Nuevos: Enseres menores
        'Compra de tostadora', 'Compra de plancha de ropa',
        'Compra de batidora de mano', 'Compra de cafetera eléctrica',
        # Nuevos: Útiles de Oficina / Ventas Adicionales
        'Venta de cuartillas de papel', 'Venta de hojas de cuartilla',
        'Compra de paquete de cuartilla', 'Adquisición de cuartilla blanca'
    ],
    'cuenta_sugerida': [
        'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina',
        'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Gasto - Servicios Básicos', 'Gasto - Servicios Básicos', 'Gasto - Servicios Básicos', 'Gasto - Servicios Básicos',
        'Gasto - Servicios Básicos', 'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        'Gasto - Limpieza y Aseo', 'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        'Activo - Mercaderías', 'Activo - Mercaderías', 'Activo - Mercaderías',
        'Gasto - Mantenimiento Vehículos', 'Gasto - Mantenimiento Vehículos', 'Gasto - Mantenimiento Vehículos',
        'Gasto - Mantenimiento Vehículos', 'Gasto - Honorarios Profesionales', 'Gasto - Honorarios Profesionales',
        'Gasto - Honorarios Profesionales', 'Gasto - Honorarios Profesionales', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Herramientas', 'Gasto - Herramientas', 'Gasto - Herramientas',
        'Gasto - Alquileres', 'Gasto - Alquileres', 'Gasto - Alquileres',
        'Ingreso - Ventas', 'Ingreso - Ventas', 'Ingreso - Servicios', 'Ingreso - Ventas', 'Ingreso - Servicios',
        'Ingreso - Servicios', 'Gasto - Combustibles', 'Gasto - Combustibles', 'Gasto - Combustibles',
        'Gasto - Seguros', 'Gasto - Representación', 'Gasto - Comisiones', 'Gasto - Software',
        'Activo Fijo - Equipos de Imagen', 'Activo Fijo - Equipos de Imagen', 'Activo Fijo - Equipos de Imagen',
        'Activo Fijo - Equipos de Imagen', 'Activo Fijo - Equipos de Imagen',
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        'Gasto - Enseres Menores', 'Gasto - Enseres Menores',
        'Gasto - Servicios Informáticos', 'Gasto - Servicios Informáticos',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Gasto - Viáticos', 'Gasto - Viáticos',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        # Nuevos: Hogar / Muebles (4)
        'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        'Activo Fijo - Muebles y Enseres', 'Activo Fijo - Muebles y Enseres',
        # Nuevos: Equipos de Computación (8)
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        'Activo Fijo - Equipos Computación', 'Activo Fijo - Equipos Computación',
        # Nuevos: Comidas y Víveres (8)
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        'Gasto - Alimentación Personal', 'Gasto - Alimentación Personal',
        # Nuevos: Productos para el hogar / Limpieza (6)
        'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        'Gasto - Limpieza y Aseo', 'Gasto - Limpieza y Aseo',
        # Nuevos: Electrodomésticos (6)
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        'Activo Fijo - Electrodomésticos', 'Activo Fijo - Electrodomésticos',
        # Nuevos: Enseres menores (4)
        'Gasto - Enseres Menores', 'Gasto - Enseres Menores',
        'Gasto - Enseres Menores', 'Gasto - Enseres Menores',
        # Nuevos: Útiles de Oficina / Ventas Adicionales (4)
        'Ingreso - Ventas', 'Ingreso - Ventas',
        'Gasto - Útiles de Oficina', 'Gasto - Útiles de Oficina'
    ]
}
