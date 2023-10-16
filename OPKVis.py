import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox
from matplotlib import style
import matplotlib as mpl

mpl.rcParams['toolbar'] = 'None'    

def rotation_matrix(omega, phi, kappa):
    omega_rad = np.radians(omega)
    phi_rad = np.radians(phi)
    kappa_rad = np.radians(kappa)

    c_omega = np.cos(omega_rad)
    s_omega = np.sin(omega_rad)
    c_phi = np.cos(phi_rad)
    s_phi = np.sin(phi_rad)
    c_kappa = np.cos(kappa_rad)
    s_kappa = np.sin(kappa_rad)

    R = np.array([
        [c_kappa * c_omega - s_kappa * c_phi * s_omega, -c_kappa * s_omega - s_kappa * c_phi * c_omega, s_kappa * s_phi],
        [s_kappa * c_omega + c_kappa * c_phi * s_omega, -s_kappa * s_omega + c_kappa * c_phi * c_omega, -c_kappa * s_phi],
        [s_phi * s_omega, s_phi * c_omega, c_phi]
    ])

    return R

def update(event=None):
    global omega, phi, kappa, ax, arrow_length, ref_arrow_length, text_area
    if event:
        if event.key == 'o':
            omega += 5
        elif event.key == 'O':
            omega -= 5
        elif event.key == 'p':
            phi += 5
        elif event.key == 'P':
            phi -= 5
        elif event.key == 'k':
            kappa += 5
        elif event.key == 'K':
            kappa -= 5

    R = rotation_matrix(omega, phi, kappa)
    ax.clear()

    # Dark background
    #ax.set_facecolor((0.1, 0.1, 0.1))

    # Reference axes (Gray color)
    ax.quiver(0, 0, 0, ref_arrow_length, 0, 0, color='gray')
    ax.quiver(0, 0, 0, 0, ref_arrow_length, 0, color='gray')
    ax.quiver(0, 0, 0, 0, 0, ref_arrow_length, color='gray')

    # Oriented axes (Red, Green, Blue colors)
    for i in range(3):
        rotated_arrow = R[:, i] * arrow_length
        ax.quiver(0, 0, 0, rotated_arrow[0], rotated_arrow[1], rotated_arrow[2], colors=['red', 'green', 'blue'][i], label=['X', 'Y', 'Z'][i])

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    plt.title('3D Orientation Visualization')
    # Customize the legend
    ax.legend(['Reference', 'X', 'Y', 'Z'],  labelcolor=['gray', 'red', 'green', 'blue'], loc='upper right', framealpha=0.7)

    # Update the text area with current values
    #text_area.set_text(f"Omega: {omega}\nPhi: {phi}\nKappa: {kappa}")
    # Add text area for controls and current values
    text_area = ax.text2D(0.02, 0.98, f"Omega: {omega}\nPhi: {phi}\nKappa: {kappa}", transform=ax.transAxes, fontsize=12, verticalalignment='top')
    fig.canvas.draw()

def update_orientation(event):
    global omega, phi, kappa
    try:
        omega = float(input_omega.text)
        phi = float(input_phi.text)
        kappa = float(input_kappa.text)
        update()
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")

def main():
    global omega, phi, kappa, arrow_length, ref_arrow_length, ax, fig, text_area, input_omega, input_phi, input_kappa
    omega = 0
    phi = 0
    kappa = 0
    arrow_length = 1.5
    ref_arrow_length = arrow_length * 0.8

    fig = plt.figure(figsize=(10, 8))  # Larger figure size
    ax = fig.add_subplot(111, projection='3d')
   
    # Dark background
    #ax.set_facecolor((0.1, 0.1, 0.1))
    #plt.style.use('dark_background')

    # make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    # Reference axes (Gray color)
    ax.quiver(0, 0, 0, ref_arrow_length, 0, 0, color='gray')
    ax.quiver(0, 0, 0, 0, ref_arrow_length, 0, color='gray')
    ax.quiver(0, 0, 0, 0, 0, ref_arrow_length, color='gray')

    # Oriented axes (Red, Green, Blue colors)
    for i in range(3):
        rotated_arrow = np.zeros(3)
        rotated_arrow[i] = arrow_length
        ax.quiver(0, 0, 0, rotated_arrow[0], rotated_arrow[1], rotated_arrow[2], colors=['red', 'green', 'blue'][i], label=['X', 'Y', 'Z'][i])

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    plt.title('3D Orientation Visualization')
    # Customize the legend
    ax.legend(['Reference', 'X', 'Y', 'Z'], loc='upper right', framealpha=0.7, labelcolor=['gray', 'red', 'green', 'blue'])

    # Add text area for controls and current values
    text_area = ax.text2D(0.02, 0.98, f"Omega: {omega}\nPhi: {phi}\nKappa: {kappa}", transform=ax.transAxes, fontsize=12, verticalalignment='top')

    # Create input fields and button
    ax_input_omega = plt.axes([0.1, 0.02, 0.2, 0.05])
    ax_input_phi = plt.axes([0.4, 0.02, 0.2, 0.05])
    ax_input_kappa = plt.axes([0.7, 0.02, 0.2, 0.05])
    input_omega = TextBox(ax_input_omega, 'Omega:', initial=str(omega))
    input_phi = TextBox(ax_input_phi, 'Phi:', initial=str(phi))
    input_kappa = TextBox(ax_input_kappa, 'Kappa:', initial=str(kappa))

    ax_update_button = plt.axes([0.1, 0.1, 0.8, 0.05])
    update_button = Button(ax_update_button, 'Update Orientation')
    update_button.on_clicked(update_orientation)

    # Connect the keyboard press event to the update function
    fig.canvas.mpl_connect('key_press_event', update)

    plt.axis('off')

    plt.show()

if __name__ == "__main__":
    main()