from PIL import Image, ImageDraw, ImageFont
import os, textwrap

# Paths
FONTS = {
    'regular': '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf',
    'medium': '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf',
    'bold': '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',
    'condensed_bold': '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf',
    'condensed': '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf',
}

# Brand colors
BLACK = (13, 13, 13)
GOLD = (184, 153, 90)
WHITE = (255, 255, 255)
BG2 = (242, 240, 236)
GRAY = (107, 104, 96)
RULE = (224, 221, 216)

W, H, PAD = 1080, 1080, 80

def font(name, size):
    return ImageFont.truetype(FONTS[name], size)

def draw_left_band(draw, color=BLACK):
    draw.rectangle([0, 0, 14, H], fill=color)

def draw_dot(draw, color=GOLD):
    cx, cy, r = int(14 + PAD * 0.6), int(PAD * 0.9), 7
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)

def draw_tag(draw, text, color=GRAY, spacing=3):
    f = font('medium', 28)
    draw.text((PAD + 14, int(PAD * 0.72)), text, font=f, fill=color)

def draw_rule(draw, y, color=RULE, width=2):
    draw.rectangle([PAD + 14, y, W - PAD, y + width], fill=color)

def draw_slide_num(draw, num, total=5, color=RULE):
    f = font('medium', 32)
    txt = f"{num}/{total}"
    bbox = draw.textbbox((0,0), txt, font=f)
    x = W - PAD // 2 - (bbox[2] - bbox[0])
    draw.text((x, int(PAD * 0.72)), txt, font=f, fill=color)

def draw_gold_bar(draw, x, y, w=100, h=6):
    draw.rectangle([x, y, x+w, y+h], fill=GOLD)

def draw_pill(draw, text, x, y):
    f = font('bold', 24)
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2] - bbox[0]
    pp = 18
    pw, ph = tw + pp*2, 48
    draw.rounded_rectangle([x, y, x+pw, y+ph], radius=6, fill=BLACK)
    draw.text((x+pp, y+10), text, font=f, fill=WHITE)
    return ph

def wrap_lines(text, max_chars=28):
    lines = []
    for para in text.split('\n'):
        if para == '':
            lines.append('')
        else:
            wrapped = textwrap.wrap(para, width=max_chars)
            lines.extend(wrapped if wrapped else [''])
    return lines

def draw_cover(post):
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    draw_left_band(draw)
    draw_dot(draw)
    draw_tag(draw, post['tag'])
    draw_rule(draw, int(PAD * 0.95))
    draw_slide_num(draw, 1)
    colors = [BLACK, GOLD, BLACK, GOLD]
    f = font('condensed_bold', 140)
    y = 300
    for i, line in enumerate(post['title']):
        draw.text((PAD + 14, y), line, font=f, fill=colors[i % 4])
        y += 158
    f_handle = font('regular', 28)
    draw.text((PAD + 14, H - int(PAD * 0.8)), '@ithinnkchile', font=f_handle, fill=GRAY)
    draw_gold_bar(draw, W - PAD//2 - 100, H - int(PAD * 0.7))
    return img

def draw_content(post, slide, num):
    img = Image.new('RGB', (W, H), BG2)
    draw = ImageDraw.Draw(img)
    draw_left_band(draw)
    draw_slide_num(draw, num, color=RULE)
    px, py = PAD + 14, int(PAD * 0.65)
    ph = draw_pill(draw, slide['pill'], px, py)
    draw_gold_bar(draw, px, py + ph + 16, w=60, h=4)
    lines = wrap_lines(slide['body'])
    f_body = font('regular', 44)
    y = py + ph + 80
    for line in lines:
        if line == '':
            y += 30
        else:
            draw.text((PAD + 14, y), line, font=f_body, fill=BLACK)
            y += 62
    f_wm = font('condensed_bold', 300)
    wm = str(num)
    bbox = draw.textbbox((0,0), wm, font=f_wm)
    wm_w = bbox[2] - bbox[0]
    wm_img = Image.new('RGBA', (wm_w + 20, 320), (0,0,0,0))
    wm_draw = ImageDraw.Draw(wm_img)
    wm_draw.text((0, 0), wm, font=f_wm, fill=(0, 0, 0, 13))
    img.paste(wm_img, (W - wm_w - PAD//2, H - 340), wm_img)
    draw_gold_bar(draw, PAD + 14, H - int(PAD * 0.7))
    return img

def draw_question(post, slide, num):
    img = Image.new('RGB', (W, H), BLACK)
    draw = ImageDraw.Draw(img)
    draw_left_band(draw, GOLD)
    f_label = font('medium', 28)
    draw.text((PAD + 14, int(PAD * 0.72)), 'PARA REFLEXIONAR', font=f_label, fill=GOLD)
    draw.rectangle([PAD+14, int(PAD*0.95), W-PAD, int(PAD*0.95)+2], fill=(184,153,90,90))
    draw_slide_num(draw, num, color=RULE)
    f_q = font('condensed_bold', 108)
    q_colors = [WHITE, GOLD, WHITE]
    lines = slide['q']
    y = 400
    for i, line in enumerate(lines):
        draw.text((PAD + 14, y), line, font=f_q, fill=q_colors[i % 3])
        y += 128
    f_wm = font('condensed_bold', 380)
    wm_img = Image.new('RGBA', (300, 400), (0,0,0,0))
    wm_draw = ImageDraw.Draw(wm_img)
    wm_draw.text((0, 0), '?', font=f_wm, fill=(184, 153, 90, 18))
    img.paste(wm_img, (W - 280, H - 420), wm_img)
    f_handle = font('regular', 26)
    draw.text((PAD + 14, H - int(PAD * 0.8)), '@ithinnkchile', font=f_handle, fill=(255,255,255,115))
    draw_gold_bar(draw, W - PAD//2 - 100, H - int(PAD * 0.7))
    return img

def generate_post(post, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    slides_data = post['slides']
    for i, slide in enumerate(slides_data):
        num = i + 1
        if slide['type'] == 'cover':
            img = draw_cover(post)
        elif slide['type'] == 'content':
            img = draw_content(post, slide, num)
        elif slide['type'] == 'question':
            img = draw_question(post, slide, num)
        path = os.path.join(output_dir, f'{prefix}_Slide{num}.png')
        img.save(path, 'PNG')
        print(f'Saved: {path}')

# ── DATA ─────────────────────────────────────────────────────────────────────

IA_POSTS = [
    {
        'tag': 'IA INDUSTRIAL',
        'title': ['IA que ve', 'mas que', 'cualquier', 'ojo humano'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL PROBLEMA','body':'En una planta de alimentos,\nuna impureza puede arruinar\ntoda una produccion.\n\nDetectarlas a tiempo era\ncaro, lento e impreciso.'},
            {'type':'content','pill':'LA SOLUCION','body':'Buhler lanzo el SORTEX AI700:\nun clasificador optico con IA\npara detectar impurezas\nen tiempo real.\n\nMenos perdidas. Mas calidad.'},
            {'type':'content','pill':'LO QUE CAMBIA','body':'Esta tecnologia ya opera\nen plantas de alimento animal\ny consumo humano.\n\nEn Chile el momento es ahora.'},
            {'type':'question','q':['Tu planta', 'depende del', 'ojo humano?']}
        ]
    },
    {
        'tag': 'IA INDUSTRIAL',
        'title': ['Robots que', 'empaquetan', 'como un', 'experto'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL DESAFIO','body':'Frutas y verduras frescas\nson irregulares por naturaleza.\n\nNingun robot tradicional\npodía manejar esa variabilidad\nsin danar el producto.'},
            {'type':'content','pill':'LA INNOVACION','body':'Chef Robotics usa vision por\ncomputadora e IA para empacar\nproductos frescos con precision.\n\nSe adapta a cada pieza\nen tiempo real.'},
            {'type':'content','pill':'EL IMPACTO','body':'Menos dependencia de mano\nde obra manual.\nMas uniformidad en producto.\n\nLineas mas eficientes\ny sostenibles.'},
            {'type':'question','q':['Cuanto cuesta', 'la variabilidad', 'en tu planta?']}
        ]
    },
    {
        'tag': 'IA INDUSTRIAL',
        'title': ['Tu planta', 'en modo', 'simulacion', 'primero'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL CONCEPTO','body':'Un gemelo digital es una\ncopia virtual de tu planta.\n\nSimula cambios, fallas\ny optimizaciones sin\ntocar nada real.'},
            {'type':'content','pill':'POR QUE IMPORTA','body':'Con IIoT e IA el gemelo\ndigital se actualiza\nen tiempo real con datos\nde tus equipos.\n\nPredice fallas antes.'},
            {'type':'content','pill':'EN LA PRACTICA','body':'Fabricantes lo usan para\nreducir paradas no planificadas.\n\nMenos downtime significa\nmas produccion y\nmejor rentabilidad.'},
            {'type':'question','q':['Ya tienes', 'un gemelo', 'de tu planta?']}
        ]
    },
    {
        'tag': 'IA INDUSTRIAL',
        'title': ['IA que', 'ensambla', 'proteinas', 'sin parar'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL RETO','body':'Manipular cortes de carne\ncruda o congelada es uno\nde los procesos mas dificiles\nde automatizar.\n\nCada pieza es diferente.'},
            {'type':'content','pill':'LA SOLUCION','body':'Chef Robotics expandio su\nplataforma al sector carnico.\n\nVision por computadora\nen tiempo real para adaptarse\na cada pieza de proteina.'},
            {'type':'content','pill':'EL RESULTADO','body':'Lineas de empaque mas\ncontinuas y eficientes.\n\nMenos errores, menos\ndesperdicio, menos\ndependencia de personal.'},
            {'type':'question','q':['La IA puede', 'entrar a tu', 'linea carnica?']}
        ]
    },
    {
        'tag': 'IA INDUSTRIAL',
        'title': ['Decisiones', 'en tiempo', 'real con', 'datos reales'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL PROBLEMA','body':'En manufactura de alta\nvariedad los datos estan\nfragmentados.\n\nDecisiones tardias cuestan\ncaro en tiempo y entrega.'},
            {'type':'content','pill':'LA HERRAMIENTA','body':'FactoryTwin combina gemelos\ndigitales con IA para\nplanificacion conectada.\n\nVisualizas tu taller completo\ndesde un solo punto.'},
            {'type':'content','pill':'LO QUE LOGRAS','body':'Mejor rendimiento medible.\nMejor cumplimiento de entrega.\n\nSin cambiar tus maquinas:\nsolo conectando los datos\nque ya tienes.'},
            {'type':'question','q':['Tus datos ya', 'trabajan', 'para ti?']}
        ]
    },
]

AF_POSTS = [
    {
        'tag': 'ANIMAL FEED',
        'title': ['Anchoveta', 'en crisis:', 'como te', 'afecta?'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL CONTEXTO','body':'Peru produce la mayor parte\nde harina de pescado\ndel mundo.\n\nCuando su temporada falla\ntodo el sector lo siente.'},
            {'type':'content','pill':'LA SITUACION','body':'Temporada 2026 es una\nde las mas bajas en\nuna decada.\n\nCuotas reducidas mas\ncombustible caro igual a\nmateria prima mas cara.'},
            {'type':'content','pill':'IMPACTO EN CHILE','body':'La formulacion de alimento\nbalanceado en acuicultura\ndepende de este ingrediente.\n\nHay que anticiparse\no pagar el precio.'},
            {'type':'question','q':['Ya tienes', 'plan B para', 'tu formula?']}
        ]
    },
    {
        'tag': 'ANIMAL FEED',
        'title': ['Proteina', 'del futuro:', 'sin pesca,', 'sin limites'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL DESAFIO','body':'La harina de pescado no\nalcanza para abastecer\nla demanda global.\n\nNecesitamos alternativas\nreales y escalables.'},
            {'type':'content','pill':'LA SOLUCION','body':'Calysseo inicio construccion\nde la primera planta\ncomercial de proteina\nunicelular FeedKind en Asia.\n\nProducida por fermentacion.'},
            {'type':'content','pill':'POR QUE IMPORTA','body':'Menos presion sobre la pesca.\nMenos volatilidad en precios.\n\nUn ingrediente sostenible\nque puede cambiar las\nformulas de salmon en Chile.'},
            {'type':'question','q':['Listo para', 'formular sin', 'harina de pez?']}
        ]
    },
    {
        'tag': 'ANIMAL FEED',
        'title': ['Camaron', 'etico:', 'el nuevo', 'estandar'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'LA NOTICIA','body':'Granjas camaroneras de\nEcuador fueron verificadas\npor cumplir estandares\nde salario digno.\n\nHito en sostenibilidad\nsocial de Latam.'},
            {'type':'content','pill':'POR QUE IMPORTA','body':'Los mercados de exportacion\nexigen trazabilidad y etica\nen toda la cadena.\n\nNo basta producir bien:\nhay que demostrarlo.'},
            {'type':'content','pill':'LA SENAL','body':'El alimento acuicola\ntambien es evaluado por\nsu impacto social.\n\nLas certificaciones son\nventaja competitiva,\nno solo un tramite.'},
            {'type':'question','q':['Tu cadena', 'de valor', 'es trazable?']}
        ]
    },
    {
        'tag': 'ANIMAL FEED',
        'title': ['Enzimas:', 'mas con', 'menos en', 'acuicultura'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL PROBLEMA','body':'Los costos de materias\nprimas para alimento\nbalanceado siguen subiendo.\n\nComo mantener el ICA\nsin quebrar la formula?'},
            {'type':'content','pill':'LA HERRAMIENTA','body':'Las proteasas mejoran\nla utilizacion de proteinas\nen el tracto digestivo.\n\nMas nutricion con\nmenos ingrediente.'},
            {'type':'content','pill':'EL RESULTADO','body':'Mejor conversion alimenticia.\nMenor dependencia de\nharina de pescado.\n\nUna palanca real para\nreducir costos sin\nbajar la calidad.'},
            {'type':'question','q':['Tus enzimas', 'estan bien', 'calibradas?']}
        ]
    },
    {
        'tag': 'ANIMAL FEED',
        'title': ['Proteinas', 'alternativas:', 'el cambio', 'ya empezo'],
        'slides': [
            {'type':'cover'},
            {'type':'content','pill':'EL ESCENARIO','body':'La escasez de harina de\npescado impulsa a la\nindustria a buscar fuentes\nalternativas de proteina.\n\nNo es tendencia: es urgencia.'},
            {'type':'content','pill':'QUE SE HACE','body':'Proyectos de I+D buscan\nescalar insectos, algas,\nlevaduras y proteina\nunicelular.\n\nPara salir de la dependencia.'},
            {'type':'content','pill':'CHILE EN EL CENTRO','body':'La industria del salmon\nnecesita alto ICA\ny sostenibilidad.\n\nAdoptar proteinas alternativas\nno es opcional:\nes el camino que viene.'},
            {'type':'question','q':['Ya estas', 'probando', 'alternativas?']}
        ]
    },
]

if __name__ == '__main__':
    out = '/home/claude/slides_output'
    print('Generando IA Industrial...')
    for i, post in enumerate(IA_POSTS):
        generate_post(post, f'{out}/IA_Industrial', f'Post{i+1}')
    print('Generando Animal Feed...')
    for i, post in enumerate(AF_POSTS):
        generate_post(post, f'{out}/Animal_Feed', f'Post{i+1}')
    print('DONE')
