from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
import textwrap
import os

def build_image(kit):
    ba, bl = 2000, 2000
    # xy, para cada posição dependendo da quantidade 
    
    fundo = Image.new( 'RGBA', (bl,ba), "white")
    carro = Image.open("car/hb20-hatch.png")
    banner = ImageDraw.Draw(fundo)
    largura, altura = fundo.size
    
    # Calculate the dimensions for the car image
    car_width, car_height = carro.size
    final_car_height = int(altura * 0.3)
    final_car_width = int(final_car_height * car_width / car_height)
    car_width = final_car_width
    car_height = final_car_height

    # Resize the car image
    carro = carro.resize((car_width, car_height))

    # Calculate the position for the car image
    car_x = int(largura * 0.25) - car_width // 2
    car_y = int(altura * 0.025)

    # Paste the car image onto the background image
    fundo.alpha_composite(im=carro, dest=(car_x, car_y))
    text = kit['nome']
    font = ImageFont.truetype("arial.ttf", 80)  
    restante = largura - (car_x + car_width + largura * 0.05 * 2)
    final_text = ''
    line = ''
    for word in text.split(' '):
        if font.getlength(final_text + ' ' + word) > restante:
            line += final_text + '\n'
            final_text = word
        else:
            final_text += ' ' + word
    
    text_width = font.getlength(final_text)
    text_x = car_x + car_width  + largura * 0.025
    text_y = (car_y + car_height) // 2 + 30
    banner.text(xy=(text_x, text_y), text=line, font=font, fill="black", align="center", spacing=30)
    
    
    shape_line = [(250, car_y + car_height + largura * 0.025), (1750, car_y + car_height + largura * 0.025)]
    banner.line(shape_line, fill="black", width=5)
    prods = len(kit['produtos'])
    match prods:
        case 1:
            print("1 item")
        case 2:
            for produto in range(prods):
                prodimagem = Image.open("product/" + kit['produtos'][produto]['cod'] + ".png")
                w, h = prodimagem.size
                w_prod = largura - largura * 0.05 * 2
                h_prod = w_prod * h // w
                prod_imagem_final = prodimagem.resize((int(w_prod), int(h_prod)))
                fundo_prod = Image.new( 'RGBA', (bl,ba), "white")
                fundo_prod.alpha_composite(im=prod_imagem_final, dest=(int(largura*0.05), int(altura//2 - h_prod//2)))
                if not os.path.exists('produtosImagens'):
                    os.makedirs("produtosImagens")
                if not os.path.exists('produtosImagens/'+kit['sku']):
                    os.makedirs('produtosImagens/'+kit['sku'])
                fundo_prod.save('produtosImagens/'+kit['sku']+'/'+kit['produtos'][produto]['cod']+".png")
                margin = largura * 0.05
                width = largura * 0.4
                height = h*width//w
                prodimagem = prodimagem.resize((int(width), int(height)))
                prodimagem_x = margin + width * produto + margin * produto * 2
                prodimagem_y = car_y + car_height + (altura - (car_y + car_height + largura * 0.025)) // 2 - height // 2
                fundo.alpha_composite(im=prodimagem, dest=(int(prodimagem_x), int(prodimagem_y)))
                if kit['produtos'][produto]['qte'] == 1:
                    text = kit['produtos'][produto]['nome']
                else:
                    text = '\n'+ str(kit['produtos'][produto]['qte']) + 'x ' + kit['produtos'][produto]['nome']
                text_width = font.getlength(text)
                text_x = prodimagem_x + width // 2 - text_width // 2
                text_y = prodimagem_y + height + altura * 0.025
                banner.text(xy=(int(text_x), int(text_y)), text=text, font=font, fill="black", align="center")    
        case 3:
            inicial = car_y + car_height
            y_inicial = inicial
            y_restante = altura - inicial
            tam_texto = 60
            for produto in range(prods):
                prodimagem = Image.open("product/" + kit['produtos'][produto]['cod'] + ".png")
                w, h = prodimagem.size
                w_prod = largura - largura * 0.05 * 2
                h_prod = w_prod * h // w
                prod_imagem_final = prodimagem.resize((int(w_prod), int(h_prod)))
                fundo_prod = Image.new( 'RGBA', (bl,ba), "white")
                fundo_prod.alpha_composite(im=prod_imagem_final, dest=(int(largura*0.05), int(altura//2 - h_prod//2)))
                if not os.path.exists('produtosImagens'):
                    os.makedirs("produtosImagens")
                if not os.path.exists('produtosImagens/'+kit['sku']):
                    os.makedirs('produtosImagens/'+kit['sku'])
                fundo_prod.save('produtosImagens/'+kit['sku']+'/'+kit['produtos'][produto]['cod']+".png")
                h_imagem = y_restante // (2.5) - largura * 0.025 * 2
                w_imagem = (h_imagem * w) // h
                prodimagem = prodimagem.resize((int(w_imagem), int(h_imagem)))
                prodimagem_x = 0
                prodimagem_y = 0
                if produto == 0:
                    prodimagem_x = largura * 0.3 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 1:
                    prodimagem_x = largura * 0.7 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 2:
                    prodimagem_x =largura // 2 - w_imagem // 2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                
                
                fundo.alpha_composite(im=prodimagem, dest=(int(prodimagem_x), int(prodimagem_y)))
                if kit['produtos'][produto]['qte'] == 1:
                    text = kit['produtos'][produto]['nome']
                else:           
                    text = '\n'+ str(kit['produtos'][produto]['qte']) + 'x ' + kit['produtos'][produto]['nome']
                font = ImageFont.truetype("arial.ttf", tam_texto)  
                text_width = font.getlength(text)   
                text_x = prodimagem_x + w_imagem // 2 - text_width // 2
                text_y = prodimagem_y + h_imagem
                banner.text(xy=(int(text_x), int(text_y)), text=text, font=font, fill="black", align="center")
        case 4:
            inicial = car_y + car_height
            y_inicial = inicial
            y_restante = altura - inicial
            tam_texto = 60
            for produto in range(prods):
                prodimagem = Image.open("product/" + kit['produtos'][produto]['cod'] + ".png")
                w, h = prodimagem.size
                w_prod = largura - largura * 0.05 * 2
                h_prod = w_prod * h // w
                prod_imagem_final = prodimagem.resize((int(w_prod), int(h_prod)))
                fundo_prod = Image.new( 'RGBA', (bl,ba), "white")
                fundo_prod.alpha_composite(im=prod_imagem_final, dest=(int(largura*0.05), int(altura//2 - h_prod//2)))
                if not os.path.exists('produtosImagens'):
                    os.makedirs("produtosImagens")
                if not os.path.exists('produtosImagens/'+kit['sku']):
                    os.makedirs('produtosImagens/'+kit['sku'])
                fundo_prod.save('produtosImagens/'+kit['sku']+'/'+kit['produtos'][produto]['cod']+".png")
                h_imagem = y_restante // (2.5) - largura * 0.025 * 2
                w_imagem = (h_imagem * w) // h
                prodimagem = prodimagem.resize((int(w_imagem), int(h_imagem)))
                prodimagem_x = 0
                prodimagem_y = 0
                if produto == 0:
                    prodimagem_x = largura * 0.3 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 1:
                    prodimagem_x = largura * 0.7 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 2:
                    prodimagem_x = largura * 0.3 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                elif produto == 3:
                    prodimagem_x = largura * 0.7 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                
                
                fundo.alpha_composite(im=prodimagem, dest=(int(prodimagem_x), int(prodimagem_y)))
                if kit['produtos'][produto]['qte'] == 1:
                    text = kit['produtos'][produto]['nome']
                else:           
                    text = '\n'+ str(kit['produtos'][produto]['qte']) + 'x ' + kit['produtos'][produto]['nome']
                font = ImageFont.truetype("arial.ttf", tam_texto)  
                text_width = font.getlength(text)   
                text_x = prodimagem_x + w_imagem // 2 - text_width // 2
                text_y = prodimagem_y + h_imagem
                banner.text(xy=(int(text_x), int(text_y)), text=text, font=font, fill="black", align="center")
        case 5:
            inicial = car_y + car_height
            y_inicial = inicial
            y_restante = altura - inicial
            tam_texto = 60
            for produto in range(prods):
                prodimagem = Image.open("product/" + kit['produtos'][produto]['cod'] + ".png")
                w, h = prodimagem.size
                w_prod = largura - largura * 0.05 * 2
                h_prod = w_prod * h // w
                prod_imagem_final = prodimagem.resize((int(w_prod), int(h_prod)))
                fundo_prod = Image.new( 'RGBA', (bl,ba), "white")
                fundo_prod.alpha_composite(im=prod_imagem_final, dest=(int(largura*0.05), int(altura//2 - h_prod//2)))
                if not os.path.exists('produtosImagens'):
                    os.makedirs("produtosImagens")
                if not os.path.exists('produtosImagens/'+kit['sku']):
                    os.makedirs('produtosImagens/'+kit['sku'])
                fundo_prod.save('produtosImagens/'+kit['sku']+'/'+kit['produtos'][produto]['cod']+".png")
                h_imagem = y_restante // (2.5) - largura * 0.025 * 2
                w_imagem = (h_imagem * w) // h
                prodimagem = prodimagem.resize((int(w_imagem), int(h_imagem)))
                prodimagem_x = 0
                prodimagem_y = 0
                if produto == 0:
                    prodimagem_x = largura * 0.2 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 1:
                    prodimagem_x = largura * 0.5 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 2:
                    prodimagem_x = largura * 0.8 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 3:
                    prodimagem_x = largura * 0.3 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                elif produto == 4:
                    prodimagem_x = largura * 0.7 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                
                
                fundo.alpha_composite(im=prodimagem, dest=(int(prodimagem_x), int(prodimagem_y)))
                if kit['produtos'][produto]['qte'] == 1:
                    text = kit['produtos'][produto]['nome']
                else:           
                    text = '\n'+ str(kit['produtos'][produto]['qte']) + 'x ' + kit['produtos'][produto]['nome']
                font = ImageFont.truetype("arial.ttf", tam_texto)  
                text_width = font.getlength(text)   
                text_x = prodimagem_x + w_imagem // 2 - text_width // 2
                text_y = prodimagem_y + h_imagem
                banner.text(xy=(int(text_x), int(text_y)), text=text, font=font, fill="black", align="center")
        case 6:
            inicial = car_y + car_height
            y_inicial = inicial
            y_restante = altura - inicial
            tam_texto = 60
            for produto in range(prods):
                prodimagem = Image.open("product/" + kit['produtos'][produto]['cod'] + ".png")
                w, h = prodimagem.size
                w_prod = largura - largura * 0.05 * 2
                h_prod = w_prod * h // w
                prod_imagem_final = prodimagem.resize((int(w_prod), int(h_prod)))
                fundo_prod = Image.new( 'RGBA', (bl,ba), "white")
                fundo_prod.alpha_composite(im=prod_imagem_final, dest=(int(largura*0.05), int(altura//2 - h_prod//2)))
                if not os.path.exists('produtosImagens'):
                    os.makedirs("produtosImagens")
                if not os.path.exists('produtosImagens/'+kit['sku']):
                    os.makedirs('produtosImagens/'+kit['sku'])
                fundo_prod.save('produtosImagens/'+kit['sku']+'/'+kit['produtos'][produto]['cod']+".png")
                h_imagem = y_restante // (2.5) - largura * 0.025 * 2
                w_imagem = (h_imagem * w) // h
                prodimagem = prodimagem.resize((int(w_imagem), int(h_imagem)))
                prodimagem_x = 0
                prodimagem_y = 0
                if produto == 0:
                    prodimagem_x = largura * 0.2 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 1:
                    prodimagem_x = largura * 0.5 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 2:
                    prodimagem_x = largura * 0.8 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.05
                elif produto == 3:
                    prodimagem_x = largura * 0.2 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                elif produto == 4:
                    prodimagem_x = largura * 0.5 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                elif produto == 5:
                    prodimagem_x = largura * 0.8 - w_imagem//2
                    prodimagem_y = y_inicial + altura * 0.025 + h_imagem + largura * 0.025 * 2 + tam_texto * 2
                
                
                fundo.alpha_composite(im=prodimagem, dest=(int(prodimagem_x), int(prodimagem_y)))
                if kit['produtos'][produto]['qte'] == 1:
                    text = kit['produtos'][produto]['nome']
                else:           
                    text = '\n'+ str(kit['produtos'][produto]['qte']) + 'x ' + kit['produtos'][produto]['nome']
                font = ImageFont.truetype("arial.ttf", tam_texto)  
                text_width = font.getlength(text)   
                text_x = prodimagem_x + w_imagem // 2 - text_width // 2
                text_y = prodimagem_y + h_imagem
                banner.text(xy=(int(text_x), int(text_y)), text=text, font=font, fill="black", align="center")
        case _:
            print("Mais de 3 itens")
        
    # Save the final image
    if not os.path.exists('produtosImagens'):
        os.makedirs("produtosImagens")
    if not os.path.exists('produtosImagens/'+kit['sku']):
        os.makedirs('produtosImagens/'+kit['sku'])
    fundo.save('produtosImagens/'+kit['sku']+'/'+kit['sku']+".png")
    

if __name__ == "__main__":
    kit={
        "sku": "HY_000009",
        "nome": "Shell Helix 1 Litro De Óleo Hx8 5w30 Motor Api Sp Sintétic",
        "produtos": [
            {
                "cod": "WO-360",
                "nome": "Filtros de Oleo'",
                "qte": 2
            },
            {
                "cod": "AKX-1100-C",
                "nome": "Filtro de Ar",
                "qte": 10
            },
            {
                "cod": "AKX-1111B",
                "nome": "Filtro de Ar",
                "qte": 10
            }  
        ]
    }
    build_image(kit)
