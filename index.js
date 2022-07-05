const { app, BrowserWindow, Menu, MenuItem } = require("electron"); 

const create_window = () => {
    const win = new BrowserWindow({
        width: 1200, 
        height: 800, 
    })

    const menu_items = [
        { label: "Exit", click() { app.exit() } },
        { label: "Visit", submenu: [
            { label: "Home", click() { win.loadFile("./web/index.html") } }, 
            { label: "Website", click() { win.loadURL("http://osamu-san.42web.io/") } }, 
            { label: "Github", click() { win.loadURL("https://github.com/osamu-kj") } }
        ]}
    ]
    const menu = Menu.buildFromTemplate(menu_items); 

    Menu.setApplicationMenu(menu)
    win.loadFile("./web/index.html");
}

app.whenReady().then(() => create_window())