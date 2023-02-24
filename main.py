from flet import *
import os
from pathlib import Path
import random

def main(page:Page):
	page.scroll="auto"
	page.padding = 0
	page.spacing = 0
	# FIND AND GET FOTO FROM FOLDER ASSETS/BURGER
	# AND CREATE DICT FROM FOLDER BURGER
	burgerlist = Row(scroll="always")
	mycounter = Text(1,size=30,weight="bold")
	youselectprice = Text(weight="bold")
	youlistorder = Column(scroll="always")



	# IF YOU SELECT THE SET WIDGET THIS
	itemselectimage = Image(width=100,height=50)
	itemselectname = Text()
	itemselectprice = Text()

	youOrder = []


	folder_path = "assets/burger/"
	files = os.listdir(folder_path)



	def youorderbtn(e):
		# AND SLIDE UP THE INCREMENT DECREMENT BUTTON Container
		conOrder.offset = transform.Offset(0,0)
		conOrder.opacity = 1
		itemselectprice.value = e.control.data['price']
		itemselectname.value = e.control.data['name']
		itemselectimage.src = e.control.data['image']

		youselectprice.value = int(mycounter.value) * int(itemselectprice.value)


		page.update()

	def decrementbtn(e):
		
		mycounter.value -=1
		youselectprice.value = int(mycounter.value) * int(itemselectprice.value)
		# AND IF YOU COUNTER < 1 OR 0 THEN SET TO 1 AGAIN
		if mycounter.value < 1: 
			mycounter.value = 1
			youselectprice.value = int(mycounter.value) * int(itemselectprice.value)
		page.update()		

	def increment(e):
		mycounter.value +=1
		youselectprice.value = int(mycounter.value) * int(itemselectprice.value)
		print(youselectprice.value)
		page.update()


	def addtocartbtn(e):
		data = {
			"name":itemselectname.value,
			"price":itemselectprice.value,
			"image":itemselectimage.src,
			"item_for_buy":mycounter.value,
			"you_buy_price":youselectprice.value

		}
		youOrder.append(data)
		print(youOrder)

		# AND AFTER CLICK . SET DEFAULT AGAIN AND CLEAR DATA
		mycounter.value = 1

		# AND SLIDE DOWN CONTAINER increment AGAIN
		conOrder.offset = transform.Offset(0,10)
		itemselectname.value = ""
		itemselectimage.src =""
		itemselectprice.value = ""
		page.update()


	def close_dialog():
		dialog.open = False
		page.update()

	dialog = AlertDialog(
		title=Text("YOu cart"),
		content=Column([

			],scroll="auto"),
		actions=[
			TextButton("close",on_click=close_dialog)
		]

		)

	def showcartbtn(e):
		for x in youOrder:
			dialog.content.controls.append(
				ListTile(
					leading=Image(x['image'],width=120,height=70),
					title=Text(x['name']),
					subtitle=Row([
						Text(f"buy pcs {x['item_for_buy']} Pcs"),
						Text(f"total price {x['you_buy_price']} "),

						])
					)

				)
		page.dialog = dialog
		dialog.open = True
		page.update()



	for file_name in files:
		if os.path.isfile(os.path.join(folder_path,file_name)):
			burger_name,ext = os.path.splitext(file_name)
			burger = {
				"name":burger_name,
				"image":os.path.join(folder_path,file_name),
				# THIS FOR FAKE RANDOM STOK FOR BURGER STOCK
				"stock":random.randint(1,20),
				# AND CREATE RANDOM PRICE FOR BURGER
				"price":random.randint(400,9000),
				"rating":round(random.uniform(1,5),1)

			}
			# AND PUSH DATA THIS DIC TO COLUMN WIDGET
			burgerlist.controls.append(
				Card(
					elevation=30,
					content=Container(
						bgcolor="white",
						width=160,
						content=Column([
						Image(src=burger['image'],
							width=160,height=140
							),
						Container(
							padding=10,
							width=160,
							bgcolor="yellow",
							border_radius=border_radius.only(topLeft=30,topRight=30),
							content=Column([
								Text(burger['name'],
									size=15,
									weight="bold"),
								Row([
									Text(f"Rate : {burger['rating']}"),
									Text(f"price : {burger['price']}"),
									],alignment="spaceBetween"),
								Row([
								ElevatedButton("Order",
								bgcolor="white",color="black",
								data=burger,
								on_click=youorderbtn
								),
								Text(f"{burger['stock']} only",
									weight="bold")

									],alignment="spaceBetween")

								])

							)

							])
						)

					)

				)
		page.update()

	# AND NOW CREATE INCREMENT AND DECREMENT BUTTON FOR BUY BURGER

	conOrder = Container(
		bgcolor="blue200",
		padding=10,
		margin=10,
		border_radius=30,
		offset=transform.Offset(0,10),
		opacity =0,
		animate_opacity=300,
		animate_offset=animation.Animation(800,curve="easeIn"),
		content=Column([
			# CREATE DECREMENT BUTTON
			Row([
				IconButton("remove",
					bgcolor="red200",
					on_click=decrementbtn
					),
				mycounter,
				IconButton("add",
					bgcolor="blue200",
					on_click=increment
					),

				],alignment="spaceBetween"),

			# SHOW SELECT IMAGE PRICE AND NAME WHEN YOU CLICK
			# ORDER BUTTON
			Row([
				itemselectimage,
				Column([
					itemselectname,
					Row([
						Text("total Price : "),
						youselectprice
						])

					]),

				]),
				# CREATE BUTTON ADD TO CART
				ElevatedButton("add to cart",
					on_click=addtocartbtn
					)


			])

		)



	page.add(
	AppBar(
	title=Text("Flet Food Order",size=30),
	bgcolor="yellow",
	actions=[
		IconButton("local_mall",
			on_click=showcartbtn
			)
	]
	),

	Column([
		Text("Burger's",size=25,weight="bold"),
		burgerlist,
		conOrder

		])

	)


flet.app(target=main,assets_dir="assets")
