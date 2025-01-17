import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import simpledialog
import zipfile

def custom_set_key(dotenv_path, key_to_set, value_to_set, quote_mode="auto", export=False):
    """
    Adds or Updates a key/value to the given .env

    If the .env path given doesn't exist, fails instead of risking creating
    an orphan .env somewhere in the filesystem
    """
    if quote_mode not in ("always", "auto", "never"):
        raise ValueError(f"Unknown quote_mode: {quote_mode}")

    quote = (
        quote_mode == "always"
        or (quote_mode == "auto" and not value_to_set.isalnum())
    )

    if quote:
        value_out = "'{}'".format(value_to_set.replace("'", "\\'"))
    else:
        value_out = value_to_set

    if export:
        line_out = f'export {key_to_set}={value_out}\n'
    else:
        line_out = f"{key_to_set}={value_out}\n"

    content = []
    replaced = False

    # Read the existing content
    with open(dotenv_path, 'r') as file:
        content = file.readlines()

    # Check and replace/add lines
    for index, line in enumerate(content):
        if line.startswith(key_to_set + '='):
            content[index] = line_out
            replaced = True
            break

    # If not replaced, append the new line
    if not replaced:
        content.append(line_out)

    # Write the content back to the .env file
    with open(dotenv_path, 'w') as file:
        file.writelines(content)

    return True, key_to_set, value_to_set

# Set default values for the other .env variables
default_values = {
    "APP_NAME": "Okul",
    "APP_ENV": "local",
    "APP_DEBUG": "false",
    #"APP_URL": "http://127.0.0.1",
    "LOG_CHANNEL": "stack",
    "LOG_DEPRECATIONS_CHANNEL": "null",
    "LOG_LEVEL": "debug",
    
    #"DB_CONNECTION": "mysql",
    #"DB_HOST": "127.0.0.1",
    #"DB_PORT": "3306",
    #"DB_DATABASE": "okul",
    #"DB_USERNAME": "root",
    #"DB_PASSWORD": "",
    
    "BROADCAST_DRIVER": "pusher",
    "CACHE_DRIVER": "file",
    "FILESYSTEM_DISK": "local",
    "QUEUE_CONNECTION": "sync",
    "SESSION_DRIVER": "database",
    "SESSION_LIFETIME": "120",
    
    "MEMCACHED_HOST": "127.0.0.1",
    
    "REDIS_HOST": "127.0.0.1",
    "REDIS_PASSWORD": "null",
    "REDIS_PORT": "6379",
    
    "MAIL_MAILER": "smtp",
    "MAIL_HOST": "mailpit",
    "MAIL_PORT": "1025",
    "MAIL_USERNAME": "null",
    "MAIL_PASSWORD": "null",
    "MAIL_ENCRYPTION": "null",
    "MAIL_FROM_ADDRESS": "hello@example.com",
    "MAIL_FROM_NAME": "${APP_NAME}",
    
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": "",
    "AWS_DEFAULT_REGION": "us-east-1",
    "AWS_BUCKET": "",
    "AWS_USE_PATH_STYLE_ENDPOINT": "false",
    
    "PUSHER_APP_ID": "testapp",
    "PUSHER_APP_KEY": "websocketkey",
    "PUSHER_APP_SECRET": "somethingsecret",
    #"PUSHER_HOST": "127.0.0.1",
    "PUSHER_PORT": "6001",
    "PUSHER_SCHEME": "http",
    "PUSHER_APP_CLUSTER": "mt1",
    
    "VITE_PUSHER_APP_KEY": "${PUSHER_APP_KEY}",
    "VITE_PUSHER_HOST": "${PUSHER_HOST}",
    "VITE_PUSHER_PORT": "${PUSHER_PORT}",
    "VITE_PUSHER_SCHEME": "${PUSHER_SCHEME}",
    "VITE_PUSHER_APP_CLUSTER": "${PUSHER_APP_CLUSTER}",
    
    "COMPANY_NAME": "Access Point IT Solutions",
    "COMPANY_MAIL": "ste.accesspoint@gmail.com",
    "COMPANY_PHONE": "+212 672 269 072",
    #"COMPANY_URL": "http://127.0.0.1:3000/"
}


class EnvDialog(simpledialog.Dialog):
    def body(self, master):
        # Define the necessary variables
        self.app_url = tk.StringVar()
        self.db_connection = tk.StringVar(value="mysql")
        self.db_host = tk.StringVar(value="127.0.0.1")
        self.db_port = tk.StringVar(value="3306")
        self.db_database = tk.StringVar()
        self.db_username = tk.StringVar(value="root")
        self.db_password = tk.StringVar()
        self.pusher_host = tk.StringVar(value="127.0.0.1")
        self.app_key = tk.StringVar(value="")
        self.company_url = tk.StringVar(value="www.accesspoint.ma")

        # Layout the input widgets
        tk.Label(master, text="APP_URL:").grid(row=0)
        tk.Entry(master, textvariable=self.app_url).grid(row=0, column=1)

        tk.Label(master, text="DB_CONNECTION:").grid(row=1)
        tk.Entry(master, textvariable=self.db_connection).grid(row=1, column=1)

        tk.Label(master, text="DB_HOST:").grid(row=2)
        tk.Entry(master, textvariable=self.db_host).grid(row=2, column=1)

        tk.Label(master, text="DB_PORT:").grid(row=3)
        tk.Entry(master, textvariable=self.db_port).grid(row=3, column=1)

        tk.Label(master, text="DB_DATABASE:").grid(row=4)
        tk.Entry(master, textvariable=self.db_database).grid(row=4, column=1)

        tk.Label(master, text="DB_USERNAME:").grid(row=5)
        tk.Entry(master, textvariable=self.db_username).grid(row=5, column=1)

        tk.Label(master, text="DB_PASSWORD:").grid(row=6)
        tk.Entry(master, textvariable=self.db_password, show="*").grid(row=6, column=1)

        tk.Label(master, text="PUSHER_HOST:").grid(row=7)
        tk.Entry(master, textvariable=self.pusher_host).grid(row=7, column=1)

        tk.Label(master, text="APP_KEY:").grid(row=8)
        tk.Entry(master, textvariable=self.app_key).grid(row=8, column=1)

        tk.Label(master, text="COMPANY_URL:").grid(row=9)
        tk.Entry(master, textvariable=self.app_key).grid(row=9, column=1)

    def apply(self):
        self.result = {
            "APP_URL": self.app_url.get(),
            "DB_CONNECTION": self.db_connection.get(),
            "DB_HOST": self.db_host.get(),
            "DB_PORT": self.db_port.get(),
            "DB_DATABASE": self.db_database.get(),
            "DB_USERNAME": self.db_username.get(),
            "DB_PASSWORD": self.db_password.get(),
            "PUSHER_HOST": self.pusher_host.get(),
            "APP_KEY": self.app_key.get(),
            "COMPANY_URL": self.company_url.get(),
        }


class App:
    def __init__(self, root):
        # Setup
        self.root = root
        self.root.title("Project Deployment")
        self.root.geometry("600x460")
        self.center_window()

        # Variables
        self.usb_path = tk.StringVar()
        self.laragon_path = tk.StringVar()
        self.status = tk.StringVar(value="Status: Waiting...")
        self.usb_path.set('')
        self.laragon_path.set("C:\\laragon\\www")

        # Title
        ttk.Label(root, text="Project Deployment Tool", font=("Helvetica", 18, "bold")).pack(pady=20)

        # USB Path Frame
        self.create_path_frame("USB Path (containing zipped folder and tools):", self.usb_path).pack(pady=10, padx=10)

        # Laragon Path Frame
        self.create_path_frame("Laragon WWW Directory:", self.laragon_path).pack(pady=10, padx=10)

        # Deploy Button
        ttk.Button(root, text="Commence Deployment", command=self.deploy).pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=10)

        # Status Label
        ttk.Label(root, textvariable=self.status).pack(pady=10)
        
        # Footer Frame
        footer_frame = tk.Frame(root)
        footer_frame.pack(pady=20)

        tk.Label(footer_frame, text="Created with ", font=("Arial", 12, "bold"), fg="#4477CE").pack(side=tk.LEFT)
        tk.Label(footer_frame, text="❤️", font=("Arial", 12, "bold"), fg="red").pack(side=tk.LEFT)
        tk.Label(footer_frame, text=" by AccessPoint IT", font=("Arial", 12, "bold"), fg="#4477CE").pack(side=tk.LEFT)

    def center_window(self):
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"+{x}+{y}")

    def create_path_frame(self, label_text, text_var):
        frame = ttk.Frame(self.root)
        ttk.Label(frame, text=label_text).pack(side="top", anchor="w")
        path_entry_frame = ttk.Frame(frame)
        path_entry_frame.pack(fill="both", expand=True, pady=5)
        ttk.Entry(path_entry_frame, textvariable=text_var, width=50).pack(side="left", padx=5)
        ttk.Button(path_entry_frame, text="Browse", command=lambda: self.browse_for_path(text_var)).pack(side="left", padx=5)
        return frame

    def browse_for_path(self, path_var):
        folder_selected = filedialog.askdirectory()
        path_var.set(folder_selected)


    def deploy(self):
        self.progress.start()

        usb_path = self.usb_path.get()
        laragon_path = self.laragon_path.get()

        if not usb_path or not laragon_path:
            messagebox.showerror("Error", "Please provide both paths!")
            return

        # Find the zip file in the usb_path and extract it to the laragon_path
        for item in os.listdir(usb_path):
            if item.endswith('.zip'):
                with zipfile.ZipFile(os.path.join(usb_path, item), 'r') as zip_ref:
                    self.status.set("Status: Extracting files...")
                    zip_ref.extractall(laragon_path)
                project_folder_name = item.rstrip('.zip')
                break
        else:
            self.status.set("Error: No zipped folder found in USB path.")
            self.progress.stop()
            return

        # Set working directory to the extracted folder
        extracted_project_path = os.path.join(laragon_path, project_folder_name)
        os.chdir(extracted_project_path)

        # Open dialog to set certain env values
        env_values = EnvDialog(self.root).result

        # Load existing .env or create one
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("")

        # Set the values obtained from the dialog
        for key, value in env_values.items():
            # If the value contains special characters or spaces, use double quotes
            if any(c in value for c in [' ', "'", '"', '\n', '\t']):
                custom_set_key('.env', key, value, quote_mode="always")
            else:
                custom_set_key('.env', key, value)

        for key, value in default_values.items():
            # If the value contains special characters or spaces, use double quotes
            if any(c in value for c in [' ', "'", '"', '\n', '\t']):
                custom_set_key('.env', key, value, quote_mode="always")
            else:
                custom_set_key('.env', key, value)


        # Install dependencies
        self.status.set("Status: Installing dependencies...")
        # os.system('composer install')
        os.system('npm install')

        # Laravel setup
        self.status.set("Status: Setting up Laravel...")
        os.system('php artisan key:generate')
        os.system('php artisan migrate --seed --force')
        os.system('php artisan storage:link')

        # Caching configurations at the end
        self.status.set("Status: Caching configurations...")
        os.system('php artisan config:clear')
        os.system('php artisan config:cache')
        os.system('php artisan route:cache')
        os.system('php artisan view:cache')
        os.system('php artisan optimize')
        
        # Frontend build (if you're using a tool like webpack or Laravel Mix)
        self.status.set("Status: Building frontend...")
        os.system('npm run build')

        # Done
        self.status.set("Status: Setup complete.")
        messagebox.showinfo("Success", "Setup completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()