
from libs.utils.common import Struct, render_template


def about(request):
    """
    关于我们
    """
    data = Struct()
    return render_template(request, 'about.html', data)




