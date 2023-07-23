import cv2
import numpy as np
from scipy import ndimage



def show(img):
    proporcao = 0.8
    nova_largura = int(img.shape[1] * proporcao)
    nova_altura = int(img.shape[0] * proporcao)
    imagem_redimensionada = cv2.resize(img, (nova_largura, nova_altura))
    cv2.imshow("show", imagem_redimensionada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#out = cv2.normalize(im_gr.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX) 
#equvalente a im2double
def im2double(im):
    min_val = np.min(im.ravel())
    max_val = np.max(im.ravel())
    out = (im.astype('float') - min_val) / (max_val - min_val)
    return out


def recognizeText(input_img_path = None,output_txt_path = None,ocr_name = None,dataset = None,flgPlot = None):
    thr_canny = 0.1
    sz_canny = 3
    sig_canny = 1
    hz_ang = 15
    vt_ang = 15
    wnd_sz = 3
    edg_den_low = 0.2
    edg_den_up = 0.5
    thr_area = np.array([1 / 20 * 1 / 15,1 / 2])
    thr_oriAng = 10
    thr_solidity = 0.65
    thr_text_hei = 20


    # plotBound = flgPlot(1)
    # plotHomo = flgPlot(2)
    # plotObj = flgPlot(3)

    img = cv2.imread(input_img_path, 0)
    im_gr = img.astype(float) / 255.0



    b_found_lines = np.array([[False,False],[False,False]])
    thetas_mm = np.array([[0,0],[0,0]])
    rhos_mm = np.array([[0,0],[0,0]])
    hei,wid = im_gr.shape

    im_gr_med = ndimage.median_filter(im_gr, size=(7, 7))
    im_gr_med = (255 * (im_gr_med - im_gr_med.min()) / (im_gr_med.max() - im_gr_med.min())).astype('uint8')


    edge_bw = cv2.Canny(im_gr_med, int(thr_canny * 255), int(sig_canny * 255))
    
    

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    edge_bw2 = cv2.dilate(edge_bw, kernel)
    
    theta_resolution = 90
    rho_resolution = 1
    lines = cv2.HoughLines(edge_bw2, rho_resolution,  np.pi / 180 * theta_resolution, 6)

    # Desenhar as linhas detectadas na imagem original (opcional)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(edge_bw2, (x1, y1), (x2, y2), 255, 1)

    edge_bw2 = cv2.filter2D(edge_bw2, -1, kernel)
    show(edge_bw2)



    


    
   
    
    
    





    

    


    





recognizeText("img/capture/0.jpg", "img/ideal")