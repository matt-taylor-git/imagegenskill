#include <QApplication>
#include <QMainWindow>
#include <QPushButton>
#include <QIcon>
#include <QVBoxLayout>
#include <QWidget>

class MainWindow : public QMainWindow {
public:
    MainWindow() {
        setWindowTitle("Imagen Skill Test - Generated Icons");
        resize(400, 300);

        // Create central widget with layout
        QWidget *centralWidget = new QWidget(this);
        QVBoxLayout *layout = new QVBoxLayout(centralWidget);
        layout->setSpacing(20);
        layout->setContentsMargins(50, 50, 50, 50);

        // Create buttons with generated icons
        QPushButton *settingsBtn = new QPushButton("Settings", this);
        settingsBtn->setIcon(QIcon(":/resources/icons/settings-icon.png"));
        settingsBtn->setIconSize(QSize(48, 48));
        settingsBtn->setMinimumHeight(80);
        settingsBtn->setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }");
        layout->addWidget(settingsBtn);

        QPushButton *profileBtn = new QPushButton("Profile", this);
        profileBtn->setIcon(QIcon(":/resources/icons/profile-icon.png"));
        profileBtn->setIconSize(QSize(48, 48));
        profileBtn->setMinimumHeight(80);
        profileBtn->setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }");
        layout->addWidget(profileBtn);

        QPushButton *helpBtn = new QPushButton("Help", this);
        helpBtn->setIcon(QIcon(":/resources/icons/help-icon.png"));
        helpBtn->setIconSize(QSize(48, 48));
        helpBtn->setMinimumHeight(80);
        helpBtn->setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }");
        layout->addWidget(helpBtn);

        // Add stretch to push buttons to top
        layout->addStretch();

        setCentralWidget(centralWidget);
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    MainWindow window;
    window.show();

    return app.exec();
}
