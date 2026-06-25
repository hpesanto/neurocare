import { Container } from "react-bootstrap";
import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";

export default function MainLayout() {
  return (
    <div className="d-flex">
      <Sidebar />
      <div className="nc-main d-flex flex-column flex-grow-1">
        <Header />
        <Container fluid className="p-4 flex-grow-1">
          <Outlet />
        </Container>
      </div>
    </div>
  );
}
