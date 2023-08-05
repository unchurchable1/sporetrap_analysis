// Check for RGB image
if (bitDepth() > 16) {
    // Convert to grayscale
    run("16-bit");
}

// Invert colors - white bg + black ROIs
run("Invert LUT");

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");

// Generate a binary image from our image stack
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light");
run("Fill Holes", "stack");
// Try to separate blobs into individual chromophores
run("Watershed");
saveAs("tif", "../binary_" + getTitle());

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "circularity=0.00-1.00 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "../results_" + File.getNameWithoutExtension(getTitle()) + ".csv");
