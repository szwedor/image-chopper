import matplotlib.pyplot as plt

def show(imgs):
    fig=plt.figure(figsize=(10, 10))
    columns = len(imgs)
    for i,img in enumerate(list(imgs)) :
        print(i)
        fig.add_subplot(1,columns, i+1)
        plt.imshow(img)
    plt.show()
    
