
jQuery.noConflict();

jQuery(document).ready(function() {
	console.log('rev begin');

    if (jQuery.fn.cssOriginal != undefined)
        jQuery.fn.css = jQuery.fn.cssOriginal;

    jQuery('.banner').revolution({
        delay: 9000,
        startheight: 500,
        startwidth: 1167,

        hideThumbs: 200,

        thumbWidth: 100,
        // Thumb With and Height and Amount (only if navigation Tyope set to thumb !)
        thumbHeight: 50,
        thumbAmount: 5,

        navigationType: "none",
        // bullet, thumb, none
        navigationArrows: "solo",
        // nexttobullets, solo (old name verticalcentered), none
        navigationStyle: "custom",
        // round,square,navbar,round-old,square-old,navbar-old, or any from the list in the docu (choose between 50+ different item), custom

        navigationHAlign: "center",
        // Vertical Align top,center,bottom
        navigationVAlign: "bottom",
        // Horizontal Align left,center,right
        navigationHOffset: 0,
        navigationVOffset: 20,

        soloArrowLeftHalign: "left",
        soloArrowLeftValign: "center",
        soloArrowLeftHOffset: 20,
        soloArrowLeftVOffset: 0,

        soloArrowRightHalign: "right",
        soloArrowRightValign: "center",
        soloArrowRightHOffset: 20,
        soloArrowRightVOffset: 0,

        touchenabled: "on",
        // Enable Swipe Function : on/off
        onHoverStop: "on",
        // Stop Banner Timet at Hover on Slide on/off
        stopAtSlide: -1,
        // Stop Timer if Slide "x" has been Reached. If stopAfterLoops set to 0, then it stops already in the first Loop at slide X which defined. -1 means do not stop at any slide. stopAfterLoops has no sinn in this case.
        stopAfterLoops: -1,
        // Stop Timer if All slides has been played "x" times. IT will stop at THe slide which is defined via stopAtSlide:x, if set to -1 slide never stop automatic
        hideCaptionAtLimit: 0,
        // It Defines if a caption should be shown under a Screen Resolution ( Basod on The Width of Browser)
        hideAllCaptionAtLilmit: 0,
        // Hide all The Captions if Width of Browser is less then this value
        hideSliderAtLimit: 0,
        // Hide the whole slider, and stop also functions if Width of Browser is less than this value
        shadow: 0,
        //0 = no Shadow, 1,2,3 = 3 Different Art of Shadows  (No Shadow in Fullwidth Version !)
        fullWidth: "off"
        // Turns On or Off the Fullwidth Image Centering in FullWidth Modus

        });

});