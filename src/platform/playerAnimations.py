cycleLength = 7
standingFrame = 4
jumpFrame = 7


# import the frame in the animation cycle. 7 frames, ordered left to right
def decideDirection(previousX, currentX, previousDirection):
    facing = None  # True = right, False = left
    if previousX is None:
        return True
    if currentX > previousX:
        facing = True
    if currentX < previousX:
        facing = False
    if currentX == previousX:
        facing = previousDirection
    return facing


# import the number of the sprite in the animation sheet, previous and current, as well as whether player is moving
def decidePlayerSprite(twoFramesAgo, previousFrame, moving):
    if twoFramesAgo == None: # Cases for nones
        if previousFrame == None:
            return standingFrame
        else:
            return standingFrame + 1
    useFrame = previousFrame
    if previousFrame > twoFramesAgo:
        if previousFrame < cycleLength:
            useFrame += 1
        else:
            useFrame -= 1
    if previousFrame < twoFramesAgo:
        if previousFrame > 1:
            useFrame -= 1
        else:
            useFrame += 1
    if twoFramesAgo == jumpFrame and previousFrame == standingFrame:
        useFrame = standingFrame + 1
    if not moving:
        useFrame = standingFrame
    return useFrame


def isInAir(previousY, currentY):
    if previousY is None:
        return False

    return previousY != currentY

def decideSprite(previousX, currentX, previousY, currentY, twoSpritesAgo, previousSprite, previousDirection):
    '''
    :param previousX, currentX, previousY, currentY: X and Y coordinates of previous frame and current frame
    :param twoSpritesAgo, previousSprite: number of sprite in sprite sheet used in last 2 frames
    :param previousDirection: last direction player was facing, True is right, False is left. None becomes True

    return:
        - frame to render
        - direction player faces, true for right, false for left
    '''
    if previousX is not None:
        moving = (previousX != currentX)
    else:
        moving = False
    if isInAir(previousY, currentY):
        return jumpFrame, decideDirection(previousX, currentX, previousDirection)
    else:
        return decidePlayerSprite(twoSpritesAgo, previousSprite, moving), decideDirection(previousX, currentX, previousDirection)

