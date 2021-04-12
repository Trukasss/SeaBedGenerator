import maya.cmds as cmds


#cmds.file(f=True,new=True)

def Fond(Stre, Freq, Ampl, colors={222,202,163}):
    cmds.file(f=True,new=True)

    # Stre=cmds.floatSliderGrp(field_strenth,q=True,v=True)
    # Freq=cmds.floatSliderGrp(field_frequency,q=True,v=True)
    # Ampl=cmds.floatSliderGrp(field_amplitude,q=True,v=True)

    #---------Creation Objet--------#
    cmds.polyCube(w=20,d=20,h=8,sx=80,sz=80,name="roche") #20 20 / 50
    cmds.polySphere(r=10,sa=60,sy=60,name="contenant") #8 / 12
    cmds.move(0,6.5,0,"contenant")
    cmds.polyBoolOp( 'contenant', 'roche', op=3, n='fond' )
    cmds.delete(ch = True)
    cmds.move(0,-4,0,"fond")


   #---------Selection Face--------#
    for i in range (0,1707):
        cmds.select("fond.f["+str(i)+"]",add=True)
        sl=cmds.ls(sl=True)

    #---------Texture Deformer--------#

    td=cmds.textureDeformer(s=Stre,ps="World",name="Textu".format(sl))
    n= cmds.shadingNode("noise".format(sl), asTexture=True)

    #--------Attributre Noise-------#
    cmds.setAttr("noise1.threshold", 0.014)
    cmds.setAttr ("noise1.amplitude",Ampl)
    cmds.setAttr( "noise1.ratio", 0.15)
    cmds.setAttr( "noise1.frequency",Freq)
    cmds.setAttr( "noise1.falloff", 1)

    cmds.connectAttr( n+".outColor", td[0]+".texture", force=True)
    
    
    Color = cmds.shadingNode('aiStandardSurface', name="colo", asShader=True)
    cmds.setAttr("colo.specular",0)
    cmds.setAttr(Color+".baseColor", colors[0], colors[1],  colors[2])
        
    cmds.select("fond",  hi=True, add=True)
    cmds.hyperShade(assign=Color)





#cmds.window()
#cmds.columnLayout()
#sliderStrenght=cmds.floatSliderGrp(field=True,label="Strenth",minValue=0,maxValue=3,value=1.5,w=400)
#sliderFreq=cmds.floatSliderGrp(field=True,label="Frequency",minValue=0,maxValue=1,value=0.3,w=400)
#sliderAmplitude=cmds.floatSliderGrp(field=True,label="Amplitude",minValue=0,maxValue=1,value=0.4,w=400)

#cmds.button(label="Fond", c="Fond()")
#cmds.showWindow()