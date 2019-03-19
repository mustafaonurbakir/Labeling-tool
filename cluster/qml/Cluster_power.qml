
import QtQuick 2.2
import QtQuick.Controls.Styles 1.4

CircularGaugeStyle {
    tickmarkInset: toPixels(0.04)
    minorTickmarkInset: tickmarkInset
    labelStepSize: 0
    labelInset: toPixels(0.00)

    property int style_mode: 1
    property real xCenter: outerRadius
    property real yCenter: outerRadius
    //property real needleLength: outerRadius - tickmarkInset * 1.25
    //property real needleTipWidth: toPixels(0.02)
    property real needleBaseWidth: toPixels(0.06)
    property bool halfGauge: false

    minimumValueAngle: -120
    maximumValueAngle: 120

    needle: Item {
        implicitWidth: __protectedScope.toPixels(0.5)
        implicitHeight: outerRadius*1.33
        y: outerRadius*0.30
        Image {
            anchors.fill: parent
            source:"images/needle3.png"
            
        }
    }

    tickmark: Rectangle {
        implicitWidth: toPixels(0.00)
        antialiasing: true
        implicitHeight: toPixels(0.00)
        color: "#c8c8c8"
    }
    minorTickmark: Rectangle {
        implicitWidth: toPixels(0.00)
        antialiasing: true
        implicitHeight: toPixels(0.00)
        color: "#c8c8c8"
    }

    function toPixels(percentage) {
        return percentage * outerRadius;
    }

    function degToRad(degrees) {
        return degrees * (Math.PI / 180);
    }

    function radToDeg(radians) {
        return radians * (180 / Math.PI);
    }

    foreground: null
}
