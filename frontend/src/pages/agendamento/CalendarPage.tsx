import { useCallback, useEffect, useMemo, useState } from "react";
import { Badge, Button, ButtonGroup, Card, Col, Form, Modal, Row, Spinner } from "react-bootstrap";
import api from "../../api/client";
import { ENDPOINTS } from "../../api/endpoints";
import FkSelect from "../../components/FkSelect";
import TimeSelect from "../../components/TimeSelect";

interface Agendamento {
  id: string;
  id_profissional: string;
  profissional_nome: string | null;
  id_paciente: string;
  paciente_nome: string | null;
  sala: number;
  data: string;
  hora_inicio: string;
  hora_fim: string;
  tipo: string;
  observacoes: string | null;
}

const PROF_COLORS = ["#2a78d6", "#1baf7a", "#9085e9", "#e34948", "#eda100", "#e87ba4", "#eb6834", "#008300"];
const SALAS = [1, 2, 3];
const TIPOS = ["Avaliacao", "Reabilitacao", "Psicoterapia", "Outro"];
const WEEKDAYS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];

function getMonday(d: Date): Date {
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  return new Date(d.getFullYear(), d.getMonth(), diff);
}

function formatDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

function addDays(d: Date, n: number): Date {
  const r = new Date(d);
  r.setDate(r.getDate() + n);
  return r;
}

function getHoursForDay(dayOfWeek: number): string[] {
  const end = dayOfWeek === 6 ? 12 : 20;
  const hours: string[] = [];
  for (let h = 7; h < end; h++) {
    hours.push(`${String(h).padStart(2, "0")}:00`);
  }
  return hours;
}

function slotSpan(inicio: string, fim: string): number {
  const [h1] = inicio.split(":").map(Number);
  const [h2] = fim.split(":").map(Number);
  return Math.max(1, h2 - h1);
}

export default function CalendarPage() {
  const [weekStart, setWeekStart] = useState(() => getMonday(new Date()));
  const [view, setView] = useState<"week" | "day">("week");
  const [dayView, setDayView] = useState(() => new Date());
  const [items, setItems] = useState<Agendamento[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Agendamento | null>(null);
  const [slotDefaults, setSlotDefaults] = useState<{ sala?: number; data?: string; hora?: string }>({});
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [profColorMap, setProfColorMap] = useState<Record<string, string>>({});

  const weekDays = useMemo(() => {
    const days: Date[] = [];
    for (let i = 0; i < 6; i++) days.push(addDays(weekStart, i));
    return days;
  }, [weekStart]);

  const fetchData = useCallback(async () => {
    setLoading(true);
    const start = view === "week" ? formatDate(weekStart) : formatDate(dayView);
    const end = view === "week" ? formatDate(addDays(weekStart, 6)) : start;
    try {
      const { data } = await api.get(`${ENDPOINTS.agendamentos}?data__gte=${start}&data__lte=${end}&page_size=200`);
      const results: Agendamento[] = data.results ?? [];
      setItems(results);
      const colorMap: Record<string, string> = {};
      const profs = [...new Set(results.map((a) => a.id_profissional))];
      profs.forEach((p, i) => { colorMap[p] = PROF_COLORS[i % PROF_COLORS.length]; });
      setProfColorMap(colorMap);
    } catch { /* empty */ }
    setLoading(false);
  }, [weekStart, dayView, view]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const openNew = (sala?: number, data?: string, hora?: string) => {
    setEditing(null);
    setSlotDefaults({ sala, data, hora });
    setError("");
    setModalOpen(true);
  };

  const openEdit = (ag: Agendamento) => {
    setEditing(ag);
    setSlotDefaults({});
    setError("");
    setModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    const fd = new FormData(e.currentTarget);
    const payload: Record<string, string | null> = {};
    fd.forEach((v, k) => { payload[k] = String(v) || null; });
    try {
      if (editing) {
        await api.patch(`${ENDPOINTS.agendamentos}${editing.id}/`, payload);
      } else {
        await api.post(ENDPOINTS.agendamentos, payload);
      }
      setModalOpen(false);
      fetchData();
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const d = (err as { response: { data: unknown } }).response.data;
        const msgs = typeof d === "object" && d ? Object.values(d as Record<string, string[]>).flat().join("; ") : "Erro ao salvar";
        setError(msgs);
      } else { setError("Erro ao salvar"); }
    }
    setSaving(false);
  };

  const handleDelete = async () => {
    if (!editing || !confirm("Excluir agendamento?")) return;
    await api.delete(`${ENDPOINTS.agendamentos}${editing.id}/`);
    setModalOpen(false);
    fetchData();
  };

  const navLabel = view === "week"
    ? `${weekStart.toLocaleDateString("pt-BR", { day: "2-digit", month: "short" })} - ${addDays(weekStart, 5).toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" })}`
    : dayView.toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long", year: "numeric" });

  return (
    <>
      <Card>
        <Card.Header className="bg-white py-3">
          <div className="d-flex justify-content-between align-items-center flex-wrap gap-2">
            <div className="d-flex align-items-center gap-2">
              <h5 className="mb-0 fw-bold"><i className="bi bi-calendar3 me-2" />Agenda</h5>
            </div>
            <div className="d-flex align-items-center gap-2">
              <ButtonGroup size="sm">
                <Button variant="outline-secondary" onClick={() => {
                  if (view === "week") setWeekStart(addDays(weekStart, -7));
                  else setDayView(addDays(dayView, -1));
                }}><i className="bi bi-chevron-left" /></Button>
                <Button variant="outline-secondary" onClick={() => {
                  setWeekStart(getMonday(new Date()));
                  setDayView(new Date());
                }}>Hoje</Button>
                <Button variant="outline-secondary" onClick={() => {
                  if (view === "week") setWeekStart(addDays(weekStart, 7));
                  else setDayView(addDays(dayView, 1));
                }}><i className="bi bi-chevron-right" /></Button>
              </ButtonGroup>
              <span className="fw-semibold small">{navLabel}</span>
              <ButtonGroup size="sm">
                <Button variant={view === "day" ? "primary" : "outline-primary"} onClick={() => setView("day")}>Dia</Button>
                <Button variant={view === "week" ? "primary" : "outline-primary"} onClick={() => setView("week")}>Semana</Button>
              </ButtonGroup>
              <Button size="sm" onClick={() => openNew()}><i className="bi bi-plus-lg me-1" />Novo</Button>
            </div>
          </div>
        </Card.Header>
        <Card.Body className="p-0" style={{ overflowX: "auto" }}>
          {loading ? (
            <div className="text-center py-5"><Spinner animation="border" /></div>
          ) : view === "week" ? (
            <div style={{ display: "grid", gridTemplateColumns: `60px repeat(${weekDays.length * 3}, 1fr)`, minWidth: 900 }}>
              {/* Header row */}
              <div className="cal-header" />
              {weekDays.map((d) => (
                <div key={d.toISOString()} className="cal-header text-center" style={{ gridColumn: `span 3`, borderBottom: "2px solid #dee2e6", padding: "8px 0" }}>
                  <div className="small text-muted">{WEEKDAYS[d.getDay()]}</div>
                  <div className="fw-bold" style={{ fontSize: 18 }}>{d.getDate()}</div>
                  <div style={{ display: "flex", justifyContent: "center", gap: 4 }}>
                    {SALAS.map((s) => <Badge key={s} bg="light" text="dark" style={{ fontSize: 9 }}>S{s}</Badge>)}
                  </div>
                </div>
              ))}
              {/* Time rows */}
              {getHoursForDay(1).map((hour) => (
                <div key={hour} style={{ height: 48, borderBottom: "1px solid #e9ecef", borderRight: "1px solid #e9ecef", padding: "2px 8px", fontSize: 11, color: "#6c757d" }}>
                  {hour}
                </div>
              ))}
              {/* This is simplified - we need per-cell rendering */}
            </div>
          ) : null}

          {/* Simpler table-based layout that actually works */}
          {!loading && (
            <table className="table table-bordered mb-0" style={{ tableLayout: "fixed" }}>
              <thead>
                {view === "week" ? (
                  <tr>
                    <th style={{ width: 60 }} />
                    {weekDays.map((d) => (
                      <th key={d.toISOString()} colSpan={3} className="text-center p-1" style={{ fontSize: 12 }}>
                        <div className="text-muted">{WEEKDAYS[d.getDay()]}</div>
                        <div className="fw-bold">{d.getDate()}/{d.getMonth() + 1}</div>
                        <div className="d-flex justify-content-center gap-1">
                          {SALAS.map((s) => <Badge key={s} bg="light" text="dark" style={{ fontSize: 9 }}>S{s}</Badge>)}
                        </div>
                      </th>
                    ))}
                  </tr>
                ) : (
                  <tr>
                    <th style={{ width: 60 }} />
                    {SALAS.map((s) => <th key={s} className="text-center">Sala {s}</th>)}
                  </tr>
                )}
              </thead>
              <tbody>
                {(view === "week" ? getHoursForDay(1) : getHoursForDay(dayView.getDay())).map((hour) => (
                  <tr key={hour} style={{ height: 48 }}>
                    <td className="text-muted text-end pe-2" style={{ fontSize: 11, verticalAlign: "top", padding: "4px 6px" }}>{hour}</td>
                    {view === "week"
                      ? weekDays.flatMap((d) =>
                          SALAS.map((sala) => {
                            const dateStr = formatDate(d);
                            const maxHour = d.getDay() === 6 ? 12 : 20;
                            const h = parseInt(hour);
                            if (h >= maxHour) return <td key={`${dateStr}-${sala}`} className="bg-light" />;
                            const ag = items.find((a) => a.data === dateStr && a.sala === sala && a.hora_inicio.slice(0, 5) === hour);
                            if (ag) {
                              const span = slotSpan(ag.hora_inicio, ag.hora_fim);
                              const color = profColorMap[ag.id_profissional] || "#6c757d";
                              return (
                                <td key={`${dateStr}-${sala}`} rowSpan={span} style={{ background: color, color: "#fff", cursor: "pointer", padding: 3, verticalAlign: "top", borderRadius: 0 }} onClick={() => openEdit(ag)}>
                                  <div style={{ fontSize: 10, fontWeight: 600 }}>{ag.paciente_nome?.split(" ")[0]}</div>
                                  <div style={{ fontSize: 9, opacity: 0.8 }}>{ag.tipo}</div>
                                </td>
                              );
                            }
                            const occupied = items.some((a) => a.data === dateStr && a.sala === sala && a.hora_inicio.slice(0, 5) < hour && a.hora_fim.slice(0, 5) > hour);
                            if (occupied) return null;
                            return <td key={`${dateStr}-${sala}`} style={{ cursor: "pointer" }} onClick={() => openNew(sala, dateStr, hour)} />;
                          })
                        )
                      : SALAS.map((sala) => {
                          const dateStr = formatDate(dayView);
                          const ag = items.find((a) => a.data === dateStr && a.sala === sala && a.hora_inicio.slice(0, 5) === hour);
                          if (ag) {
                            const span = slotSpan(ag.hora_inicio, ag.hora_fim);
                            const color = profColorMap[ag.id_profissional] || "#6c757d";
                            return (
                              <td key={sala} rowSpan={span} style={{ background: color, color: "#fff", cursor: "pointer", padding: 6, verticalAlign: "top" }} onClick={() => openEdit(ag)}>
                                <div className="fw-bold" style={{ fontSize: 12 }}>{ag.paciente_nome}</div>
                                <div style={{ fontSize: 11, opacity: 0.85 }}>{ag.profissional_nome}</div>
                                <div style={{ fontSize: 10, opacity: 0.7 }}>{ag.tipo} | {ag.hora_inicio.slice(0, 5)}-{ag.hora_fim.slice(0, 5)}</div>
                              </td>
                            );
                          }
                          const occupied = items.some((a) => a.data === dateStr && a.sala === sala && a.hora_inicio.slice(0, 5) < hour && a.hora_fim.slice(0, 5) > hour);
                          if (occupied) return null;
                          return <td key={sala} style={{ cursor: "pointer" }} onClick={() => openNew(sala, dateStr, hour)} />;
                        })
                    }
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card.Body>
      </Card>

      {/* Legend */}
      {Object.keys(profColorMap).length > 0 && (
        <div className="d-flex gap-3 mt-2 flex-wrap">
          {items.filter((a, i, arr) => arr.findIndex((x) => x.id_profissional === a.id_profissional) === i).map((a) => (
            <span key={a.id_profissional} className="d-flex align-items-center gap-1" style={{ fontSize: 12 }}>
              <span style={{ width: 12, height: 12, borderRadius: 2, background: profColorMap[a.id_profissional] }} />
              {a.profissional_nome}
            </span>
          ))}
        </div>
      )}

      {/* Modal */}
      <Modal show={modalOpen} onHide={() => setModalOpen(false)} centered backdrop="static" keyboard={false}>
        <form onSubmit={handleSubmit}>
          <Modal.Header closeButton>
            <Modal.Title as="h5">{editing ? "Editar Agendamento" : "Novo Agendamento"}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Row className="g-3">
              <Col md={6}>
                <FkSelect name="id_profissional" label="Profissional" endpoint={ENDPOINTS.profissionais} labelField="nome" defaultValue={editing?.id_profissional} required />
              </Col>
              <Col md={6}>
                <FkSelect name="id_paciente" label="Paciente" endpoint={ENDPOINTS.pacientes} labelField="nome_completo" defaultValue={editing?.id_paciente} required />
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Sala *</Form.Label>
                  <Form.Select name="sala" defaultValue={editing?.sala ?? slotDefaults.sala ?? ""} required>
                    <option value="">Selecione</option>
                    <option value="1">Sala 1</option>
                    <option value="2">Sala 2</option>
                    <option value="3">Sala 3</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Data *</Form.Label>
                  <Form.Control name="data" type="date" defaultValue={editing?.data ?? slotDefaults.data ?? ""} required />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Tipo *</Form.Label>
                  <Form.Select name="tipo" defaultValue={editing?.tipo ?? "Psicoterapia"} required>
                    {TIPOS.map((t) => <option key={t} value={t}>{t}</option>)}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <TimeSelect name="hora_inicio" label="Hora Inicio *" defaultValue={editing?.hora_inicio ?? slotDefaults.hora} required />
              </Col>
              <Col md={6}>
                <TimeSelect name="hora_fim" label="Hora Fim *" defaultValue={editing?.hora_fim} required />
              </Col>
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Observacoes</Form.Label>
                  <Form.Control as="textarea" rows={2} name="observacoes" defaultValue={editing?.observacoes ?? ""} />
                </Form.Group>
              </Col>
            </Row>
            {error && <div className="alert alert-danger mt-3 mb-0 py-2">{error}</div>}
          </Modal.Body>
          <Modal.Footer>
            {editing && (
              <Button variant="outline-danger" onClick={handleDelete} className="me-auto">
                <i className="bi bi-trash me-1" />Excluir
              </Button>
            )}
            <Button variant="secondary" onClick={() => setModalOpen(false)}>Cancelar</Button>
            <Button variant="primary" type="submit" disabled={saving}>
              {saving ? <Spinner animation="border" size="sm" /> : <><i className="bi bi-check-lg me-1" />Salvar</>}
            </Button>
          </Modal.Footer>
        </form>
      </Modal>
    </>
  );
}
