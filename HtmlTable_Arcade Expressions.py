def TableCellConfiguration( BaseValue , **DesignModifiers ):
	
    def HTMLFormatting( element , modifiers , value ):
        n = '\n'
        t = '\t'
        elements = {
            'row' : f'{ n }{ t*3 }<tr>{ value }{ n }{ t*3 }</tr>',
            'header' : f'{ n }{ t*4 }<th { modifiers }>{ value }{ n }{ t*4 }</th>',
            'data' : f'{ n }{ t*4 }<td { modifiers }>{ value }{ n }{ t*4 }</td>',
            'paragraph' : f'{ n }{ t*5 }<p { modifiers }>{ value }</p>',
            'span' : f'<span { modifiers }>{ value }</span>'
            }
        return elements[ element ]

    DefaultElementOrder = [ 'span' , 'paragraph' , 'data' , 'header' , 'row' ]

    tdhtml = None
    for element in DefaultElementOrder:
        Design = DesignModifiers[ element ]
        if tdhtml is None: tdhtml = HTMLFormatting( element , Design , BaseValue )
        else: tdhtml = HTMLFormatting( element , Design , tdhtml )
        
    return tdhtml

def HTMLFormatting( element , modifiers , value ):
    n = '\n'
    t = '\t'
    elements = {
        'rows' : f'{ n }{ t*2 }<tr>{ value }{ n }{ t*2 }</tr>',
        'headers' : f'{ n }{ t*2 }<th { modifiers }>{ value }{ n }{ t*2 }</th>',
        'data' : f'{ n }{ t*3 }<td { modifiers }>{ value }{ n }{ t*3 }</td>',
        'paragraph' : f'{ n }{ t*4 }<p { modifiers }>{ value }</p>',
        'span' : f'<span { modifiers }>{ value }</span>'
        }
    return elements[ element ]

def HTMLTable( Design , Body ): return f'<table{ Design }>\n\t<tbody>\t{ Body }\n\t</tbody>\n</table>'

def SetFormat( **formatting ):
    formats = [
        'border',
        'cellpadding',
        'cellspacing',
        'colspan',
        'rowspan'
        ]
    return ' '.join( [ f'{ cellformat }="{ formatting[ cellformat ] }"' for cellformat in formatting if cellformat in formats ] )

def SetStyle( **styling ):
    styles = {
        'backgroundcolor' : 'background-color',
        'bordercollapse' : 'border-collapse',
        'width' : 'width',
        'textalign' : 'text-align',
        'fontsize' : 'font-size',
        'color' : 'color',
        'borderstyle' : 'border-style',
        'bordercolor' : 'border-color',
        'border' : 'border'
        }
    styleformat = '; '.join( [ f'{ styles[ style ] }: { styling[ style ] }' for style in styling if styling[ style ] ] )
    return  f'style="{ styleformat }"'

def BorderStyle( size , bordertype , color ):  return f'{ size }px { bordertype } { color }'

def Modifiers( formatting , styling ): return f'{ formatting } { styling }'

def ReferenceText( text ): return f'{ "{" }{ text }{ "}" }'

def TextFormatting( TextFormat , Text ):
    Formats = {
        'bold' : f'<strong>{Text}</strong>',
        'italicize' : f'<i>{Text}</i>',
        'quote' : f'<q>{Text}</q>'
        }
    return Formats[ TextFormat ]

# set table style and format
TStyle = SetStyle( width = '100%' , backgroundcolor = '#d9e1f2' , bordercollapse = 'border-collapse' )
TFormat = SetFormat( border='1' , cellpadding='5' , cellspacing='0' )
TableDesign = f'{ TFormat } { TStyle }'


# cells in table
TableColumns = 7
TableRows = 6
TableCells = [ i for i in range( TableColumns * TableRows ) ]
CellRows = 4

# set cell values
Replace = 'Replace'
BackgroundColor = [ ReferenceText( f'expression/{ x }T' ) for x in TableCells ]
BaseElements = [
    TextFormatting( 'bold' , ReferenceText( f'D{ Replace }' ) ),
    TextFormatting( 'bold' , ReferenceText( f'C{ Replace }' ) ),
    TextFormatting( 'bold' , ReferenceText( f'expression/{ Replace }A' ) )
    ]
BaseElements = [ [ y.replace( Replace , str(x) ) for y in BaseElements ] for x in TableCells ]
LabelElements = [ 'Inspections' , 'Shift' ]

# cell layout
def TableCellConfiguration( Styles , Formats ):
    span = HTMLFormatting( 'span' , spanstyle , Value )
    p = HTMLFormatting( 'paragraph' , pstyle , span )
    td = HTMLFormatting( 'data' , f'{ tdformat } { tdstyle }' , p )
    return

# create design elements
TableCellDesign = { }

for i in TableCells:
    
    # Values
    Day , Count , Shift = BaseElements[ i ]
    BGColor = BackgroundColor[ i ]

    # Defaults
    pstyle = SetStyle( textalign = "center" )

    # cell formatting and styling
    CellValueDesign = { }
    for Value in BaseElements[ i ]:
        tdformat = ''
        tdstyle = SetStyle( border =  BorderStyle( 1 , 'solid' , 'black' ) , width = '.25%' , backgroundcolor = BGColor )
        spanstyle = SetStyle( fontsize = '10' )
        
        if Value == Day:
            tdformat = SetFormat( rowspan="4" )
            tdstyle = SetStyle( border =  BorderStyle( 1 , 'solid' , 'black' ) , width = 'Calc(100%/7)' , backgroundcolor = BGColor )
            spanstyle = SetStyle( fontsize = '32' )

        # set values
        span = HTMLFormatting( 'span' , spanstyle , Value )
        p = HTMLFormatting( 'paragraph' , pstyle , span )
        td = HTMLFormatting( 'data' , f'{ tdformat } { tdstyle }' , p )
        CellValueDesign[ Value ] = td

    LabelDesign = { }
    for label in LabelElements:
        TextFormatting( 'bold' , label )
        tdformat = ''
        tdstyle = SetStyle( border =  BorderStyle( 1 , 'solid' , 'black' ) , width = '.25%' , backgroundcolor = BGColor )
        spanstyle = SetStyle( fontsize = '10' )

        span = HTMLFormatting( 'span' , spanstyle , label )
        p = HTMLFormatting( 'paragraph' , pstyle , span )
        td = HTMLFormatting( 'data' , f'{ tdformat } { tdstyle }' , p )
        LabelDesign[ label ] = td

    # combine single row
    Combine = CellValueDesign[ Day ] + LabelDesign[ 'Inspections' ]

    CellRowDesign = { }
    for row in range( CellRows ):
        if row == 0: CellRowDesign[ row ] = Combine
        elif row == 1: CellRowDesign[ row ] = CellValueDesign[ Count ]
        elif row == 2 : CellRowDesign[ row ] = LabelDesign[ 'Shift' ]
        else: CellRowDesign[ row ] = CellValueDesign[ Shift ]
            
    TableCellDesign[ i ] = CellRowDesign
    

# create sublist of list consisting of row and column values as subsets
RowSets = [ TableCells[ i : TableColumns ] if i == 0 else TableCells[ TableColumns*i : TableColumns*(i+1) ] for i in range( TableRows ) ]
TableBody = [ ]
for row in RowSets:
    for cellrow in range( CellRows ):
        ConcatValues = [ ]
        for column in row:
            crows = TableCellDesign[ column ]
            ConcatValues += [ crows[ cellrow ] ]
        ConcatValues = ''.join( ConcatValues )
        TableBody += [ HTMLFormatting( 'rows' , '' , ConcatValues ) ]
TableBody = ''.join( TableBody )
        
OutputHTML = HTMLTable( TableDesign, TableBody )
print( OutputHTML )
