## 项目介绍
Django搭建的一个半成品网站，方便学习和快速建站。内含一个随机点单的app，用户输入资金上限，即可通过线性规划生成满足要求的具体点单菜品组合~
![](https://lijiaweinpc.github.io/static/%E7%94%B1%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90gif/showcase.gif)

## 项目优势
- 功能简洁单一，模块划分清楚，方便了解和学习django的MVC结构，路由系统等；方便基于此结构进行二次开发。
- 预置了一版KFC的菜单，可以方便的查看APP1_LP/appfiles/ITEM_CATEGORY.xlsx了解详情，准备类似的价格表并调用APP1_LP/hisrand_gen.py更新网站库，生成假历史订单。

## 快速开始
- 进入项目根目录并pip安装好依赖: pip install -r requirements.txt
- 执行命令启动server： python manage.py runserver
- 浏览器打开: http://127.0.0.1:8000/
