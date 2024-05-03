import { useEffect, useState } from "react";
import FoodCard from "../components/FoodCard";
import AddFoodButton from "../components/AddFoodButton";

interface Food {
  id: number;
  name: string;
  expiration_date: string;
}

export default function ListFood() {
  const [foods, setFoods] = useState<Food[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/list")
      .then((response) => response.json())
      .then((data) => setFoods(data));
  }, []);

  function calculateDaysLeft(expirationDate: string): number {
    const expiration = new Date(expirationDate);
    const today = new Date();
    const timeDifference = expiration.getTime() - today.getTime();
    const daysLeft = Math.ceil(timeDifference / (1000 * 3600 * 24));
    return daysLeft;
  }

  function handleDelete(id: number) {
    fetch("http://localhost:8000/delete_food/" + id.toString(), {
      method: "DELETE",
      headers: {},
    });

    setFoods(foods.filter((food) => food.id !== id));
  }

  function handleEdit() {
    console.log("Edit");
  }

  return (
    <div className="w-full h-full">
      <header className="h-[10vh]">
        <h1>Food Academy</h1>
      </header>
      <div className="flex flex-col justify-between h-[85vh]">
        <div className="flex-nowrap max-h-[80vh] overflow-auto max-w-full overflow-x-hidden ">
          {foods.map((food) => (
            <FoodCard
              key={food.id}
              name={food.name}
              expiresIn={calculateDaysLeft(food.expiration_date).toString()}
              onDelete={() => handleDelete(food.id)}
              onEdit={handleEdit}
            />
          ))}
        </div>
        <footer>
          <AddFoodButton />
        </footer>
      </div>
    </div>
  );
}
