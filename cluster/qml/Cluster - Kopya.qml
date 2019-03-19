
import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQml 2.0
import QtGraphicalEffects 1.0



Window {
    id: pencere
    visible: true
    //visibility: Window.FullScreen
    height: 384
    width: 1024
    onWindowStateChanged: {
        console.log( "onWindowStateChanged (Window), state: " + windowState );
    }

    FontLoader {id: pt_narrow; source: "pt-sans/PTN57F.ttf"}
    FontLoader {id: pt_bold; source: "pt-sans/PTS76F.ttf"}

    //color: "#161616"
    color: "black"
    title: "CLUSTER"




    //hız, guc, charge, gear bilgileri geliyor
    ValueSource {
        id: value_source
    }
    //iki mod arasinda gecisleri, nesnelerin boyutlarındaki degisim bilgisi geliyor
    
    //cluster ortasindaki menu bilgisi geliyor




    Item {
        id: container
        width: pencere.width
        height: Math.min(pencere.width, pencere.height)
        visible: true
        opacity: 1
        anchors.centerIn: parent

        Image {
            id: mainbackground
            width: 1024
            height: 466
            anchors.verticalCenterOffset: 0
            anchors.horizontalCenterOffset: 0
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            fillMode: Image.PreserveAspectFit
            sourceSize.height: 400
            sourceSize.width: 1024
            source: "images/Automotive_ClusterScreen_background_2-46.png"
            visible: true
            z: 0
            opacity: 1
        }

        Image {
            id: alt_ust_image
            //x: 0
            //y: 67
            width: 1024
            height: 466
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            fillMode: Image.PreserveAspectFit
            sourceSize.height: 400
            sourceSize.width: 1024
            source: "images/alt_ust.png"
            visible: true
            z: 2
            opacity: 1
        }

        //gauges images
        Image {
            id: speedimage
            //x: 0
            //y: 67
            width: 1024
            height: 320
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenterOffset: -322
            anchors.verticalCenterOffset: 0
            fillMode: Image.PreserveAspectFit
            sourceSize.height: 400
            sourceSize.width: 1024
            source: "images/Automotive_ClusterScreen_KM_Gage_1-46.png"
            visible: true
            z: 4
            opacity: 1
        }
        Image {
            id: powerimage
            //x: 0
            //y: 67
            width: 1024
            height: 320
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            fillMode: Image.PreserveAspectFit
            anchors.horizontalCenterOffset: 320
            anchors.verticalCenterOffset: 0
            sourceSize.height: 400
            sourceSize.width: 1024
            source: "images/Automotive_ClusterScreen_PowerGage_1-47.png"
            visible: true
            z: 5
            opacity: 1
        }
        //gauges rings
        Image {
            id: speedimagering
            //x: 0
            //y: 67
            width: 1000
            height: 318
            anchors.horizontalCenter: speedimage.horizontalCenter
            anchors.verticalCenter: speedimage.verticalCenter
            anchors.verticalCenterOffset: 2
            anchors.horizontalCenterOffset: -1
            fillMode: Image.PreserveAspectFit
            sourceSize.height: 400
            sourceSize.width: 1024
            source: "images/Automotive_ClusterScreen_Gear_Borderframe-47.png"
            visible: true
            z: 9
            opacity: 1
        }

        // hiz ve power ibre
        Item {
            id: gaugeItem
            z: 5
            //spacing: container.width * 0.02
            anchors.centerIn: parent

            CircularGauge {
                id: speedometer
                width: 315
                height: 315
                value: value_source.imagine_kph
                anchors.verticalCenter: parent.verticalCenter
                maximumValue: 260
                stepSize: 0
                anchors.horizontalCenterOffset: -322
                anchors.verticalCenterOffset: 3    //ileride bu 3ü relative yap
                anchors.horizontalCenter: parent.horizontalCenter
                z:4

                style: Cluster_kph {
                    style_mode: 1

                }

                Text {
                    id: speedText
                    text: value_source.kph.toFixed(0)
                    font.family: pt_narrow.name
                    font.pixelSize: 80

                    anchors.verticalCenterOffset: speedometer.horizontalCenter
                    anchors.verticalCenter: speedometer.verticalCenter
                    anchors.horizontalCenterOffset: 0
                    color: "white"
                    horizontalAlignment: Text.AlignRight
                    anchors.horizontalCenter: speedometer.horizontalCenter
                    visible: true

                    function set() {
                        speedText.text = value_source.kph.toFixed(0);
                    }
                }

            }

            CircularGauge {
                id: powermeter
                width: 315
                height: 315
                value: value_source.power
                anchors.verticalCenter: parent.verticalCenter
                maximumValue: 100
                minimumValue: 0
                stepSize: 0
                anchors.horizontalCenterOffset: 321
                anchors.verticalCenterOffset: 1
                anchors.horizontalCenter: parent.horizontalCenter
                z:4

                style: Cluster_power {
                    style_mode: 1
                }

                Text {
                    id: powerText
                    text: "%" + value_source.power.toFixed(0)
                    font.family: pt_narrow.name
                    font.pixelSize: 40

                    anchors.verticalCenterOffset: powermeter.horizontalCenter
                    anchors.verticalCenter: powermeter.verticalCenter
                    anchors.horizontalCenterOffset: 0
                    color: "white"
                    horizontalAlignment: Text.AlignRight
                    anchors.horizontalCenter: powermeter.horizontalCenter
                    visible: true
                    function set2() {
                        powerText.text = "<font size='1'>"+"%" + "</font>" + "<font size='6'>"+value_source.power.toFixed(0) + "</font>";
                    }
                }

            }



            Timer {
                id: texttimer
                interval: 200
                repeat: true
                running: true
                triggeredOnStart: true
                onTriggered: powerText.set2() & speedText.set()
            }

        }


    }
}

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
