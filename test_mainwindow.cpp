#include <QApplication>
#include <QPushButton>
#include <QIcon>
#include <QMainWindow>

class MainWindow : public QMainWindow {
public:
    MainWindow() {
        // Empty icons - Imagen skill will fill these!
        QPushButton settingsBtn("Settings");
        settingsBtn.setIcon(QIcon(":/resources/icons/settings-icon.png"));

        QPushButton profileBtn("Profile");
        profileBtn.setIcon(QIcon(":/resources/icons/profile-icon.png"));

        QPushButton helpBtn("Help");
        helpBtn.setIcon(QIcon(":/resources/icons/help-icon.png"));
    }
};
