# Document_Scanner_using_opencv
creating a cam scanner using opencv to detect the document in an image and present it in front of the user.

Our task is to take an image and detect the paper object in it that is our document, like cam scanner app which puts a boundary around the paper object in the image.

so first we start by importing the image aand resizing it to a particular size to slightly ease up the processing, then after that applying blur opeartion on the image in order to reduce the noise present in the image but in a controlled way so that the other important details don't get lost, there after applying edge transformation (Canny) to get the edges , after that getting  the boundaries of various objects present in the image using the find contour function and we are only concerned with the boundaries of length 4 as we assume our document to be a square or rectangle

After getting the boundary of that document appplying the perspective transform in order to get a top viw of the paper, by taking the new pixel information by making sum assumptions like new values of co-ordiantes and their min and max values.

In the last step thresholding is applied so as to get a clear view of the document by applying simple thresholding and adaptive thresholding.
