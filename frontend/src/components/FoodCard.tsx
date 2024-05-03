import { FaTrash } from "react-icons/fa";
import { MdOutlineEdit } from "react-icons/md";

interface FoodCardProps {
  name: string;
  expiresIn: string;
  onDelete: () => void;
  onEdit: () => void;
}

export default function FoodCard(props: FoodCardProps) {
  return (
    <div className="justify-center w-[99%] grid grid-cols-[1fr_7fr] border border-white rounded-xl hover:bg-slate-700 p-4 m-2 hover:shadow-md hover:shadow-white transition-all hover:cursor-pointer">
      <div className="flex justify-center items-center">
        <h5 className="text-xl">{props.name}</h5>
      </div>
      <div className="flex flex-row justify-end items-center">
        <p className="text-xl align-middle text-center justify-center m-2 text-gray-400">
          Expires in {props.expiresIn} days
        </p>
        <IconButton color="red" onClick={props.onDelete}>
          <FaTrash />
        </IconButton>

        <IconButton color="blue" onClick={props.onEdit}>
          <MdOutlineEdit />
        </IconButton>
      </div>
    </div>
  );
}

function IconButton(props: {
  onClick: () => void;
  color: string;
  children: React.ReactNode;
}) {
  return (
    <button
      className={`w-max m-2 hover:bg-${props.color}-600 hover:transition-all hover:shadow hover:shadow-${props.color}-300`}
      onClick={props.onClick}
    >
      {props.children}
    </button>
  );
}
